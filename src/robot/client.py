import socket # Phyton에서 네트워크 통신 기능 사용
import json # Phyton에서 네트워크 통신 기능 사용

HOST = "127.0.0.1" # 서버 IP 주소
PORT = 5000 # 서버와 동일한 포트 번호 사용

user_input = input("Enter command (open/close/move/status): ") # 사용자로부터 명령어 입력
parts = user_input.split() # 입력된 명령어를 공백으로 분리하여 리스트로 저장

if len(parts) == 1: # 입력된 명령어가 없는 경우 오류 메시지 출력
    request = {"cmd": parts[0]} # 명령어를 JSON 형식으로 변환
elif len(parts) == 2 and parts[0].lower() == "move": # 입력된 명령어가 "move"이고 각도가 포함된 경우
    try:
        angle = int(parts[1]) # 각도 파라미터를 정수로 변환
        request = {"cmd": parts[0], "angle": angle} # 명령어와 각도를 JSON 형식으로 변환
    except ValueError: # 각도 파라미터가 정수가 아닌 경우 오류 메시지 출력
        print("Invalid angle. Please enter an integer between 0 and 180.")
        exit(1)
else: # 입력된 명령어가 유효하지 않은 경우 오류 메시지 출력
    print("Invalid command. Please enter 'open', 'close', 'move <angle>', or 'status'.")
    exit(1)
client_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 클라이언트 소켓 생성
client_soket.connect((HOST, PORT)) # 서버에 연결
client_soket.sendall(json.dumps(request).encode()) # 서버로 명령어 전

request = client_soket.recv(1024) # 서버로부터 응답 수신
print("Response:",json.loads(request.decode()))
client_soket.close() # 소켓 닫기

""" # v.0.2 - 클라이언트에서 명령어를 JSON 형식으로 변환하여 서버로 전송
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 클라이언트 소켓 생성
client_socket.connect((HOST, PORT)) # 서버에 연결

while True:
    cmd = input("Send command (open/close/status): ") # 사용자로부터 명령어 입력

    data = {"cmd": cmd} # 명령어를 JSON 형식으로 변환
    msg = json.dumps(data)  # JSON 문자열로 변환
    
    client_socket.sendall(msg.encode()) # 서버로 명령어 전송

    response = client_socket.recv(1024).decode() # 서버로부터 응답 수신
    print("Response: ", response) # 응답 출력

client_socket.close() # 소켓 닫기

"""
