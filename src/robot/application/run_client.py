from robot.config.settings import settings # 설정값을 별도의 변수로 임포트
from robot.interface.tcp_client import TCPClient # TCP 클라이언트 클래스 임포트

def create_client_app():
    client = TCPClient(settings.TCP_HOST, settings.TCP_PORT)
    return client

def main():
    client = create_client_app() # TCP 클라이언트 애플리케이션 생성
    
    while True: # 무한 루프를 돌며 사용자 입력 처리
        user_input = input("Enter command (or 'exit' to quit): ") # 사용자로부터 명령어 입력 받기
        if user_input.lower() == "exit": # 사용자가 "exit"를 입력한 경우 루프 종료
            print("Exiting client application.")
            break
        
        response = client.send_command(user_input) # 명령어 전송 및 응답 수신
        print(f"Response from server: {response}") # 서버로부터 받은 응답 출력

if __name__ == "__main__":
    main() # main 함수 호출하여 애플리케이션 시작