import socket
import threading

HOST = '192.168.1.100'  # Change to host's IP address
PORT = 5000

def handle_receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print("\nHost:", data.decode())
        except ConnectionResetError:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

recv_thread = threading.Thread(target=handle_receive, args=(client,), daemon=True)
recv_thread.start()

while True:
    try:
        msg = input("You: ")
        client.sendall(msg.encode())
    except (BrokenPipeError, KeyboardInterrupt):
        break

client.close()
