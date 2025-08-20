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
        
    def add_or_update_player(self, remote_addr, state):
        with self.players_lock:
            self.players[remote_addr] = state
    
    def get_players(self):
        with self.players_lock:
            return self.players.copy()
    
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
                    *_, last_line = buffer.strip().split('\n')
                    ip, port = conn.getpeername()
                    remote_x, remote_y = map(int, last_line.strip().split(","))
                    self.add_or_update_player(f"{ip}:{port}", (remote_x, remote_y))
                    buffer = ""
            except:
                traceback.print_exc()
        conn.close()
    
    def send_position(self, x, y):
        if self.client_mode and self.client:
            self.client.sendall(f"\n{x},{y}".encode())
    
    def is_client_mode(self):
        return self.client_mode
    
    def get_clients(self):
        return self.clients
