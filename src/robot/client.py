import socket

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    cmd = input("Send command (open/close/status): ")
    client_socket.sendall(cmd.encode())

    data = client_socket.recv(1024)
    print("Response:", data.decode())

client_socket.close()