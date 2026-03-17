import socket                           # Phyton에서 네트워크 통신 기능 사용 
from state_machine import RobotState

HOST = "127.0.0.1"
PORT = 5000

robot = RobotState()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    cmd = data.decode()
    
    result = robot.handle_command(cmd)
    conn.sendall(result.encode())
conn.close()
server_socket.close()
