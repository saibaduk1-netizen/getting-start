import json
import socket

from robot.config.settings import settings # 설정값을 별도의 변수로 임포트
class TCPClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_command(self, command: dict) -> dict:
        request_data = json.dumps(command).encode("utf-8") # 명령어를 JSON 형식으로 직렬화하여 바이트로 인코딩

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port)) # TCP 서버에 연결
            client_socket.sendall(request_data) # 요청 데이터 전송
            
            response_data = client_socket.recv(settings.TCP_BUFFER_SIZE) # 서버로부터 응답 데이터 수신
            response_text = response_data.decode("utf-8") # 응답 데이터를 UTF-8 문자열로 디코딩
            response = json.loads(response_text) # 응답 텍스트를 JSON으로 파싱하여 딕셔너리로 변환
            
            return response