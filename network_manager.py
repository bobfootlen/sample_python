import socket
import threading
import traceback

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

    def add_or_update_player(self, player_id, remote_addr, x, y, face):
        with self.players_lock:
            self.players[player_id] = {'addr': remote_addr, 'x': x, 'y': y, 'face': face}

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
        return True

    def setup_server(self):
        self.client_mode = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', self.port))
        self.server.listen(1)
        print("Waiting for connection...")

        def accept_loop():
            while True:
                self.accept_one()

        def accept_one():
            conn, addr = self.server.accept()
            print("Connected by", addr)
            self.clients.append(conn)
            threading.Thread(target=self.handle_receive, args=(conn,), daemon=True).start()

        threading.Thread(target=accept_one, daemon=True).start()

    def handle_receive(self, conn):
        buffer = ""
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                buffer += data.decode()
                if '\n' in buffer:
                    lines = buffer.strip().split('\n')
                    for line in lines:
                        try:
                            player_id_str, remote_x_str, remote_y_str, face = line.strip().split(",")
                            player_id = int(player_id_str)
                            remote_x = int(remote_x_str)
                            remote_y = int(remote_y_str)
                            ip, port = conn.getpeername()
                            self.add_or_update_player(player_id, f"{ip}:{port}", remote_x, remote_y, face)
                        except ValueError:
                            print(f"Malformed player data received: {line}")
                    buffer = ""
            except:
                traceback.print_exc()
        conn.close()

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
            for conn in self.clients:
                try:
                    conn.sendall(message.encode())
                except Exception as e:
                    print(f"Error broadcasting to client: {e}")
