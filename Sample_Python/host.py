import socket
import threading

HOST = ''
PORT = 5000

def handle_receive(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print("\nClient:", data.decode())
        except ConnectionResetError:
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("Waiting for connection...")
conn, addr = server.accept()
print("Connected by", addr)

recv_thread = threading.Thread(target=handle_receive, args=(conn,), daemon=True)
recv_thread.start()

while True:
    try:
        msg = input("You: ")
        conn.sendall(msg.encode())
    except (BrokenPipeError, KeyboardInterrupt):
        break

conn.close()
