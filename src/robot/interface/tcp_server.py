import socket

from robot.config.settings import settings # 설정값을 별도의 변수로 임포트
from robot.infrastructure.tcp_protocol import ( ProtocolError, parse_request, build_response)
from robot.services import command_service # TCP 프로토콜 관련 함수와 예외 클래스 임포트

class TCPServer:
    def __init__(self, host: str, port: int, command_service):
        self.host = host
        self.port = port
        self.command_service = command_service

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: # TCP 소켓 생성
            server_socket.bind((self.host, self.port)) # 소켓을 호스트와 포트에 바인딩
            server_socket.listen() # 클라이언트 연결 대기
            print(f"TCP Server listening on {self.host}:{self.port}")

            while True: # 무한 루프를 돌며 클라이언트 연결 처리
                client_socket, addr = server_socket.accept() # 클라이언트 연결 수락
                print(f"Accepted connection from {addr}")
                with client_socket: # 클라이언트 소켓을 컨텍스트 매니저로 사용하여 자동으로 닫히도록 함
                  print(f"[TCPServer] Connection from {addr}")
                  self.handle_client(client_socket) # 클라이언트 요청 처리
    
    def handle_client(self, client_socket):
            raw_data = client_socket.recv(settings.TCP_BUFFER_SIZE) # 클라이언트로부터 데이터 수신
            try:
                command = parse_request(raw_data) # 수신된 데이터를 요청으로 파싱
                self.command_service.submit_command(command) # 명령어 처리
                command = {"result": "OK", "message": "Command received"} # 명령어가 정상적으로 처리된 경우 응답 페이로드 생성
            except ProtocolError as exc: # 프로토콜 오류가 발생한 경우 예외 처리
                command = {"result": "Error", "message": str(exc)} # 오류 메시지를 응답 페이로드에 포함
            except ValueError as exc: # 명령어 형식이 유효하지 않은 경우 예외 처리
                command = {"result": "Error", "message": str(exc)} # 오류 메시지를 응답 페이로드에 포함
            except Exception as exc: # 기타 예외가 발생한 경우 예외 처리
                command = {"result": "Error", "message": f"Internal server error: {exc}"} # 일반적인 서버 오류 메시지를 응답 페이로드에 포함
                
            client_socket.sendall(build_response(command)) # 응답을 JSON 형식으로 빌드하여 클라이언트로 전송


