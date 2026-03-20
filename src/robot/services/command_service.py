from robot.domain.robot_state import RobotState # 로봇 상태 클래스 임포트
from robot.domain.state_machine import StateMachine # 상태 머신 클래스 임포트

class CommandService:
    def __init__(self, command_queue, state_machine: StateMachine, robot_state: RobotState): # CommandService 클래스의 초기화 메서드 정의, 명령어 큐, 상태 머신, 로봇 상태를 인자로 받아 초기화
        self.state_machine = state_machine # CommandService 클래스의 인스턴스가 생성될 때 StateMachine 인스턴스를 초기화하여 명령어 처리를 담당
        self.robot_state = robot_state # CommandService 클래스의 인스턴스가 생성될 때 RobotState 인스턴스를 초기화하여 로봇 상태를 관리
        self.command_queue = command_queue # CommandService 클래스의 인스턴스가 생성될 때 명령어 큐를 초기화하여 명령어를 비동기적으로 처리할 수 있도록 함

    def submit_command(self, command: dict) -> None: # 명령어를 제출하는 메서드 정의, 입력은 딕셔너리 형태의 명령어, 출력도 딕셔너리 형태의 결과
        self._validate_command_shape(command) # 명령어의 형식을 검증하는 별도의 메서드를 호출하여 명령어의 유효성을 검증
        self.command_queue.put(command) # 명령어 큐에 명령어를 추가하여 비동기적으로 처리할 수 있도록 함

    def process_command(self, command: dict) -> dict: # 명령어를 처리하는 메서드 정의, 입력은 딕셔너리 형태의 명령어, 출력도 딕셔너리 형태의 결과
        return self.state_machine.handle_command(self.robot_state, command) # 상태 머신의 handle_command 메서드를 호출하여 명령어를 처리하고 결과를 반환

    def _validate_command_shape(self, command: dict) -> bool: # 명령어의 형식을 검증하는 별도의 메서드 정의, 명령어가 딕셔너리 형태인지 확인하여 유효성 검증
        if not isinstance(command, dict):
            raise ValueError("Command must be a dictionary") # 명령어가 딕셔너리가 아닌 경우 예외 발생
        elif "command" not in command:
            raise ValueError("Command must include 'command' field") # 명령어에 "command" 키가 없는 경우 예외 발생
        elif not isinstance(command["command"], str):
            raise ValueError("Command 'command' value must be a string") # "command" 키의 값이 문자열이 아닌 경우 예외 발생
        return True # 명령어 형식이 유효한 경우 True 반환

        