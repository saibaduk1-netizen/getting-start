import pytest
from robot.domain.robot_state import RobotState
from robot.domain.state_machine import StateMachine
from robot.services.command_service import CommandService

class DummyQueue: # 명령어 큐의 동작을 시뮬레이션하기 위한 더미 큐 클래스 정의, 실제 큐 대신 테스트에서 사용할 수 있도록 간단한 구현 제공
    def __init__(self):
        self.item = []
    def put(self, item):
        self.item.append(item)

def test_submit_puts_command_into_queue(): # CommandService의 submit_command 메서드가 명령어를 큐에 올바르게 추가하는지 테스트하는 함수 정의, DummyQueue를 사용하여 명령어가 큐에 추가되는지 검증
    queue = DummyQueue() 
    state_machine = StateMachine() 
    robot_state = RobotState()
    command_service = CommandService(queue, state_machine, robot_state) # CommandService 인스턴스 생성, 더미 큐, 상태 머신, 로봇 상태를 인자로 전달
    
    command = {"command": "open"} # 테스트할 명령어 정의
    command_service.submit_command(command) # CommandService의 submit_command 메서드를 호출하여 명령어 제출
    
    assert queue.item[0] == command # DummyQueue에 추가된 명령어가 제출한 명령어와 동일한지 검증

def test_process_command_delegates_to_state_machine(): # CommandService의 process_command 메서드가 명령어 처리를 StateMachine의 handle_command 메서드에 위임하는지 테스트하는 함수 정의, 상태 머신과 로봇 상태를 사용하여 명령어 처리 결과를 검증
    queue = DummyQueue()
    state_machine = StateMachine()
    robot_state = RobotState()
    command_service = CommandService(queue, state_machine, robot_state) # CommandService 인스턴스 생성, 더미 큐, 상태 머신, 로봇 상태를 인자로 전달
    
    command = {"command": "open"} # 테스트할 명령어 정의
    result = command_service.process_command(command) # CommandService의 process_command 메서드를 호출하여 명령어 처리 결과 얻음
    
    assert result["result"] == "OK" # 처리 결과가 "OK"인지 검증
    assert result["state"] == "OPEN" # 처리 결과에 포함된 그리퍼 상태가 "OPEN"인지 검증
    assert robot_state.gripper_state == "OPEN" # 로봇의 그리퍼 상태가 "OPEN"으로 변경되었는지 검증

def test_submit_command_raises_for_non_dict(): # CommandService의 submit_command 메서드가 명령어가 딕셔너리가 아닌 경우 예외를 발생시키는지 테스트하는 함수 정의, 명령어 형식이 유효하지 않은 경우 예외 발생을 검증
    queue = DummyQueue()
    state_machine = StateMachine()
    robot_state = RobotState()
    command_service = CommandService(queue, state_machine, robot_state) # CommandService 인스턴스 생성, 더미 큐, 상태 머신, 로봇 상태를 인자로 전달
    
    with pytest.raises(ValueError, match="Command must be a dictionary"): # 명령어가 딕셔너리가 아닌 경우 ValueError 예외가 발생하는지 검증
        command_service.submit_command("not a dict") # 문자열 형태의 명령어 제출하여 예외 발생 검증

def test_submit_command_raises_when_command_missing(): # CommandService의 submit_command 메서드가 명령어에 'command' 키가 없는 경우 예외를 발생시키는지 테스트하는 함수 정의, 명령어 형식이 유효하지 않은 경우 예외 발생을 검증
    queue = DummyQueue()
    state_machine = StateMachine()
    robot_state = RobotState()
    command_service = CommandService(queue, state_machine, robot_state) # CommandService 인스턴스 생성, 더미 큐, 상태 머신, 로봇 상태를 인자로 전달
    
    with pytest.raises(ValueError, match="Command must include 'command' field"): # 명령어에 'command' 키가 없는 경우 ValueError 예외가 발생하는지 검증
        command_service.submit_command({"mode": "absolute"}) # 'command' 키가 없는 명령어 제출하여 예외 발생 검증
    
def test_submit_command_raises_when_command_not_string(): # CommandService의 submit_command 메서드가 명령어의 'command' 키의 값이 문자열이 아닌 경우 예외를 발생시키는지 테스트하는 함수 정의, 명령어 형식이 유효하지 않은 경우 예외 발생을 검증
    queue = DummyQueue()
    state_machine = StateMachine()
    robot_state = RobotState()
    command_service = CommandService(queue, state_machine, robot_state) # CommandService 인스턴스 생성, 더미 큐, 상태 머신, 로봇 상태를 인자로 전달
    
    with pytest.raises(ValueError, match="Command 'command' value must be a string"): # 명령어의 'command' 키의 값이 문자열이 아닌 경우 ValueError 예외가 발생하는지 검증
        command_service.submit_command({"command": 123}) # 'command' 키의 값이 정수인 명령어 제출하여 예외 발생 검증