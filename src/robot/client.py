import socket # Phyton에서 네트워크 통신 기능 사용
import json # Phyton에서 네트워크 통신 기능 사용

HOST = "127.0.0.1" # 서버 IP 주소
PORT = 5000 # 서버와 동일한 포트 번호 사용

user_input = input("Enter command (open/close/move/status): ") # 사용자로부터 명령어 입력
parts = user_input.split() # 입력된 명령어를 공백으로 분리하여 리스트로 저장

if len(parts) == 1: # 입력된 명령어가 없는 경우 오류 메시지 출력
    request = {"cmd": parts[0].lower()} # 명령어를 JSON 형식으로 변환
elif len(parts) == 3 and parts[0].lower() == "move": # 입력된 명령어가 "move"이고 각도가 포함된 경우
    cmd = parts[0].lower() # 명령어를 소문자로 변환
    mode = parts[1].lower() # 이동 모드를 소문자로 변환
    angle = int(parts[2]) # 각도 문자열 추출

    if mode == "absolute":
        request = {"cmd": cmd, "mode": mode, "angle": angle} # 명령어와 각도를 JSON 형식으로 변환
    elif mode == "relative":
        request = {"cmd": cmd, "mode": mode, "delta": angle} # 명령어와 각도 변화량을 JSON 형식으로 변환
    else: # 이동 모드가 유효하지 않은 경우 오류 메시지 출력
        print("Invalid move mode. Please add 'absolute' or 'relative'.")
        exit(1)
else: # 입력된 명령어가 유효하지 않은 경우 오류 메시지 출력
    print("Invalid command. Please enter 'open', 'close', 'move <mode> <angle>', or 'status'.")
    exit(1)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 클라이언트 소켓 생성
client_socket.connect((HOST, PORT)) # 서버에 연결
client_socket.sendall(json.dumps(request).encode()) # 서버로 명령어 전

request = client_socket.recv(1024) # 서버로부터 응답 수신
print("Response:",json.loads(request.decode()))
client_socket.close() # 소켓 닫기
