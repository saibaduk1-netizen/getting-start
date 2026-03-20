import threading
from robot.domain.robot_state import RobotState # 로봇 상태 클래스 임포트
from robot.domain.state_machine import StateMachine # 상태 머신 클래스 임포트
from robot.infrastructure.command_queue import CommandQueue # 명령어 큐 클래스 임포트
from robot.infrastructure.worker import Worker # 작업자 클래스 임포트
from robot.interface.tcp_server import TCPServer # TCP 서버 클래스 임포트
from robot.services.command_service import CommandService # 명령어 서비스 클래스 임포트
from robot.config.settings import settings # 설정값을 별도의 변수로 임포트

def main():
    host = settings.TCP_HOST # TCP 서버 호스트 설정값 가져오기
    port = settings.TCP_PORT # TCP 서버 포트 설정값 가져오기

    robot_state = RobotState() # 로봇 상태 인스턴스 생성
    state_machine = StateMachine() # 상태 머신 인스턴스 생성
    command_queue = CommandQueue() # 명령어 큐 인스턴스 생성
    command_service = CommandService(command_queue, state_machine, robot_state) # 명령어

    worker = Worker(command_queue, command_service) # 작업자 인스턴스 생성
    worker_thread = threading.Thread(target=worker.run_forever, daemon=True) # 작업자 스레드 생성, 데몬 스레드로 설정하여 메인 스레드가 종료될 때 자동으로 종료되도록 함
    worker_thread.start() # 작업자 스레드 시작 

    server = TCPServer(host, port, command_service) # TCP 서버 인스턴스 생성
    server.serve_forever() # TCP 서버 무한 루프 시작

    if __name__ == "__main__":
        main() # main 함수 호출하여 애플리케이션 시작
