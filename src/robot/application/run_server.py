from robot.config.settings import settings # 설정값을 별도의 변수로 임포트

from robot.domain import robot_state
from robot.domain.state_machine import StateMachine # 상태 머신 클래스 임포트
from robot.services.command_service import CommandService # 명령어 서비스 클래스 임포트
from robot.infrastructure.command_queue import CommandQueue # 명령어 큐 클래스 임포트
from robot.interface.tcp_server import TCPServer # TCP 서버 클래스 임포트

def create_server_app():
    state_machine = StateMachine() # 상태 머신 인스턴스 생성
    command_queue = CommandQueue() # 명령어 큐 인스턴스 생성
    command_service = CommandService(command_queue, state_machine, robot_state) # 명령어 서비스 인스턴스 생성
    tcp_server = TCPServer(
        settings.TCP_HOST, settings.TCP_PORT, command_service) # TCP 서버 인스턴스 생성
    return tcp_server
    

def main():
    server = create_server_app() # TCP 서버 애플리케이션 생성
    server.start() # TCP 서버 시작

    if __name__ == "__main__":
        main() # main 함수 호출하여 애플리케이션 시작
