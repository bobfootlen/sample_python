import socket
import threading
import time

class NetworkManager:
    def __init__(self, port=5000):
        self.port = port
        self.players = {}
        self.players_lock = threading.Lock()
        self.clients = []
        self.client = None
        self.server = None
        self.client_mode = False
        self.local_players_ref = None # To hold reference to local players from Game
        self.next_player_id = 1  # Initialize a counter for unique player IDs
        self.conn_to_player_id = {} # Map connection objects to server-assigned player IDs

    def add_or_update_player(self, player_id, remote_addr, x, y, face):
        with self.players_lock:
            self.players[player_id] = {'addr': remote_addr, 'x': x, 'y': y, 'face': face, 'last_seen': time.time()}

    def get_players(self):
        with self.players_lock:
            return self.players.copy()

    def set_local_players_ref(self, players):
        self.local_players_ref = players

    def setup_client(self, host, username):
        self.client_mode = True
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, self.port))
        print("Connected.")
        threading.Thread(target=self.handle_receive_client, args=(self.client,), daemon=True).start()
        return True


    def handle_receive_client(self, conn):
        buffer = ""
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                buffer += data.decode()
                if '\n' in buffer:
                    lines = buffer.strip().split('\n')
                    updated_players = []
                    for line in lines:
                        try:
                            client_sent_player_id_str, remote_x_str, remote_y_str, face = line.strip().split(",")
                            remote_x = int(remote_x_str)
                            remote_y = int(remote_y_str)
                            self.add_or_update_player(client_sent_player_id_str, f"{conn.getpeername()[0]}:{conn.getpeername()[1]}", remote_x, remote_y, face)
                            updated_players.append(client_sent_player_id_str)
                        except ValueError:
                            print(f"Malformed player data received from {conn.getpeername()}: {line}")
                    buffer = ""
                    self.purge_stale_players(updated_players)
            except:
                pass
        conn.close()
        
    def purge_stale_players(self, updated_players):
        """
        Remove players that are no longer active (not in the updated_players list).
        Also remove players that haven't been seen for more than 10 seconds.
        """
        current_time = time.time()
        stale_timeout = 10.0  # Remove players after 10 seconds of inactivity
        
        with self.players_lock:
            # Create a list of players to remove to avoid modifying dict during iteration
            players_to_remove = []
            
            for player_id, player_data in self.players.items():
                # Check if player is not in the updated list (not recently active)
                if player_id not in updated_players:
                    # Check if player has been inactive for too long
                    time_since_last_seen = current_time - player_data.get('last_seen', 0)
                    if time_since_last_seen > stale_timeout:
                        players_to_remove.append(player_id)
                        print(f"Removing stale player {player_id} (inactive for {time_since_last_seen:.1f}s)")
            
            # Remove stale players
            for player_id in players_to_remove:
                del self.players[player_id]


    def setup_server(self):
        self.client_mode = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', self.port))
        self.server.listen(1)
        print("Waiting for connection...")

        def accept_loop():
            while True:
                self.accept_one()

        threading.Thread(target=accept_loop, daemon=True).start()

    def accept_one(self):
        conn, addr = self.server.accept()
        print("Connected by", addr)
        self.clients.append(conn)

        # Assign a unique player ID to this connection
        server_assigned_player_id = self.next_player_id
        self.conn_to_player_id[conn] = server_assigned_player_id
        self.next_player_id += 1
        print(f"Assigned player ID {server_assigned_player_id} to {addr}")

        threading.Thread(target=self.handle_receive_server, args=(conn,), daemon=True).start()

    def handle_receive_server(self, conn):
        buffer = ""
        peer_addr = conn.getpeername()
        # Retrieve the server-assigned player ID for this connection
        server_assigned_player_id = self.conn_to_player_id.get(conn)

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f"Client {peer_addr} (Player ID: {server_assigned_player_id}) disconnected.")
                    break
                buffer += data.decode()
                if '\n' in buffer:
                    lines = buffer.strip().split('\n')
                    for line in lines:
                        try:
                            # We still parse the client's data, but we will use our server-assigned ID
                            client_sent_player_id_str, remote_x_str, remote_y_str, face = line.strip().split(",")
                            # player_id = int(client_sent_player_id_str) # This line is no longer used for updating self.players

                            remote_x = int(remote_x_str)
                            remote_y = int(remote_y_str)
                            # Use the server-assigned player_id to update the players dictionary
                            self.add_or_update_player(server_assigned_player_id, f"{peer_addr[0]}:{peer_addr[1]}", remote_x, remote_y, face)
                        except ValueError:
                            print(f"Malformed player data received from {peer_addr} (Player ID: {server_assigned_player_id}): {line}")
                    buffer = ""
            except:
                pass # This block handles other unexpected connection issues
        conn.close()
        # Remove client from self.clients
        if conn in self.clients:
            self.clients.remove(conn)
        # Remove from conn_to_player_id as well
        if conn in self.conn_to_player_id:
            disconnected_player_id = self.conn_to_player_id[conn]
            del self.conn_to_player_id[conn]
        else:
            disconnected_player_id = None # Should not happen if logic is correct

        # Remove player associated with this connection from self.players
        with self.players_lock:
            if disconnected_player_id and disconnected_player_id in self.players:
                del self.players[disconnected_player_id]
                print(f"Removed player {disconnected_player_id} due to disconnect.")
            # The previous logic that iterated through self.players based on addr is now redundant.

    def send_position(self, player_id, x, y, face):
        if self.client_mode and self.client:
            self.client.sendall(f"\n{player_id},{x},{y},{face}".encode())

    def is_client_mode(self):
        return self.client_mode

    def get_clients(self):
        return self.clients

    def broadcast_player_states(self):
        if not self.client_mode and self.server:
            all_player_states = []
            # Add local players' states
            if self.local_players_ref:
                for player in self.local_players_ref:
                    all_player_states.append(f"{player.player_id},{player.x},{player.y},{player.face}")

            # Add remote players' states (which server already knows)
            with self.players_lock:
                for player_id, player_data in self.players.items():
                    all_player_states.append(f"{player_id},{player_data['x']},{player_data['y']},{player_data['face']}")

            message = "\n" + "\n".join(all_player_states)
            disconnected_clients = []
            for conn in self.clients:
                try:
                    conn.sendall(message.encode())
                except (BrokenPipeError, ConnectionResetError) as e:
                    print(f"Client {conn.getpeername()} disconnected during broadcast: {e}")
                    disconnected_clients.append(conn)
                except Exception as e:
                    print(f"Error broadcasting to client {conn.getpeername()}: {e}")
            for conn in disconnected_clients:
                self.clients.remove(conn)
                # Remove from conn_to_player_id
                if conn in self.conn_to_player_id:
                    disconnected_player_id = self.conn_to_player_id[conn]
                    del self.conn_to_player_id[conn]
                    
                    # Remove the player from self.players using the stored player_id
                    with self.players_lock:
                        if disconnected_player_id in self.players:
                            del self.players[disconnected_player_id]
                            print(f"Removed player {disconnected_player_id} due to broadcast disconnect.")

