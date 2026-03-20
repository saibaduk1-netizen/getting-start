import socket    # Phyton에서 네트워크 통신 기능 사용
import json
import threading     # Phyton에서 네트워크 통신 기능 사용 

from queue import Queue    # 파이썬에서 큐 자료구조 사용
from robot.getting_start._state_machine import RobotState    # 로봇 상태 머신 클래스 임포트

HOST = "127.0.0.1"   # 서버 IP 주소 (로컬호스트)
PORT = 5000         # 서버와 동일한 포트 번호 사용

def worker():   # 명령어 큐에서 명령어를 처리하는 워커 스레드 함수 정의
    while True:     # 무한 루프를 사용하여 큐에서 명령어를 계속 처리
        cmd = cmd_queue.get()     # 큐에서 명령어 가져오기 (큐가 비어있으면 대기)
        if cmd is None:   # 종료 신호로 None이 전달된 경우 루프 탈출
            break
        result = robot.handle_command(cmd)    # 로봇 상태 머신에서 명령어 처리 결과를 반환
        print("Processed command:", cmd, "Response:", result)   # 처리된 명령어와 응답을 출력
        cmd_queue.task_done()    # 큐에 있는 작업이 완료되었음을 알림


robot = RobotState()    # 로봇 상태 머신 인스턴스 생성
cmd_queue = Queue()     # 명령어 큐 생성

threading.Thread(target=worker, daemon=True).start()    # 워커 스레드 시작 (데몬 스레드로 설정하여 메인 프로그램 종료 시 자동으로 종료되도록 함)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 서버 소켓 생성 
server_socket .setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # 서버 소켓 옵션 설정 (주소 재사용 허용)
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
            cmd_queue.put(request)     # 명령어를 큐에 추가
            response = {"result": "QUEUED", "message": "Command accepted"}    # 명령어가 큐에 추가되었음을 나타내는 응답 딕셔너리 생성
# V0.5삭제            response = robot.handle_command(request) # 로봇 상태 머신에서 명령어 처리 결과를 반환
        except Exception as e:            # 예외가 발생한 경우 오류 메시지를 포함한 결과 딕셔너리 생성
            response = {"result": "ERROR", "message": str(e)} # 오류 메시지를 포함한 결과 딕셔너리 생성
        conn.sendall(json.dumps(response).encode())    # 클라이언트에 JSON 형식의 응답 전송
conn.close()                # 클라이언트 연결 소켓 닫기
server_socket.close()       # 서버 소켓 닫기
