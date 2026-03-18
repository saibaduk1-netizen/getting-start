import socket    # Phyton에서 네트워크 통신 기능 사용
import json     # Phyton에서 네트워크 통신 기능 사용 
from state_machine import RobotState    # 로봇 상태 머신 클래스 임포트

HOST = "127.0.0.1"   # 서버 IP 주소 (로컬호스트)
PORT = 5000         # 서버와 동일한 포트 번호 사용

robot = RobotState()    # 로봇 상태 머신 인스턴스 생성

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 서버 소켓 생성 
server_socket.bind((HOST, PORT))    # 서버 소켓을 지정된 IP 주소와 포트 번호에 바인딩
server_socket.listen(1)     # 서버 소켓이 클라이언트 연결을 수신 대기하도록 설정 (최대 1개의 연결 허용)

print(f"Server listening on {HOST}:{PORT}")      # 서버가 지정된 IP 주소와 포트 번호에서 클라이언트 연결을 수신 대기 중임을 출력

while True:         # 무한 루프를 사용하여 클라이언트로부터 명령어를 계속 수신
    conn, addr = server_socket.accept()     # 서버 소켓이 클라이언트 연결을 수락하고, 연결된 클라이언트의 소켓 객체와 주소 정보를 반환
    with conn:       # 클라이언트 연결 소켓을 컨텍스트 매니저로 사용하여 자동으로 닫히도록 함
        data = conn.recv(1024)      # 클라이언트로부터 데이터를 수신 (최대 1024 바이트)
        if not data:        # 클라이언트가 연결을 종료한 경우 루프 탈출
            continue
    
        try:            # 수신된 명령어를 JSON 형식으로 파싱하여 로봇 상태 머신에 전달 
            request = json.loads(data.decode())             # JSON 문자열을 파이썬 딕셔너리로 변환
            response = robot.handle_command(request) # 로봇 상태 머신에서 명령어 처리 결과를 반환
        except Exception as e:            # 예외가 발생한 경우 오류 메시지를 포함한 결과 딕셔너리 생성
            response = {"RESULT": "ERROR", "MESSAGE": str(e)} # 오류 메시지를 포함한 결과 딕셔너리 생성
        # response = json.dumps(result)           # 결과 딕셔너리를 JSON 문자열로 변환하여 클라이언트에 응답으로 전송
        conn.sendall(json.dumps(response).encode())    # 클라이언트에 JSON 형식의 응답 전송
conn.close()                # 클라이언트 연결 소켓 닫기
server_socket.close()       # 서버 소켓 닫기
