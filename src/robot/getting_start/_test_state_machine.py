import pytest # pytest 라이브러리 임포트
from robot.getting_start._state_machine import RobotState # 로봇 상태 머신 클래스 임포트

@pytest.fixture # pytest에서 테스트 함수에 사용할 수 있는 고정된 상태를 제공하는 fixture 정의
def robot(): # 테스트 함수에서 사용할 RobotState 인스턴스를 생성하여 반환하는 fixture
    return RobotState()

def test_open(robot): # "open" 명령어에 대한 테스트 함수 정의
    result = robot.handle_command({"cmd": "open"}) # "open" 명령어를 처리하는 메서드 호출
    assert result["result"] == "OK" # 결과가 "OK"인지 확인
    assert result["state"] == "OPEN" # 상태가 "OPEN"인지 확인

def test_close(robot): # "close" 명령어에 대한 테스트 함수 정의
    robot.handle_command({"cmd": "open"}) # 먼저 "open" 명령어를 처리하여 상태를 "OPEN"으로 변경
    result = robot.handle_command({"cmd": "close"}) # "close" 명령어를 처리하는 메서드 호출
    assert result["state"] == "CLOSED" # 상태가 "CLOSED"인지 확인

def test_move_absolute(robot): # "move" 명령어에 대한 테스트 함수 정의 (절대 모드)
    result = robot.handle_command({"cmd": "move", "mode": "absolute", "angle": 90}) # "move" 명령어를 절대 모드로 처리하는 메서드 호출
    assert result["angle"] == 90 # 각도가 90인지 확인

def test_move_relative(robot): # "move" 명령어에 대한 테스트 함수 정의 (상대 모드)
    robot.handle_command({"cmd": "move", "mode": "absolute", "angle": 90}) # 먼저 "move" 명령어를 절대 모드로 처리하여 각도를 90으로 설정
    result = robot.handle_command({"cmd": "move", "mode": "relative", "delta": -30}) # "move" 명령어를 상대 모드로 처리하는 메서드 호출
    assert result["angle"] == 60 # 각도가 60인지 확인 (90에서 -30만큼 이동)

def test_invalid_command(robot): # 유효하지 않은 명령어에 대한 테스트 함수 정의
    result = robot.handle_command({"cmd": "invalid"}) # "invalid" 명령어를 처리하는 메서드 호출
    assert result["result"] == "Error" # 결과가 "Error"인지 확인

def test_angle_out_of_range(robot): # 각도가 범위를 벗어나는 경우에 대한 테스트 함수 정의
    result = robot.handle_command({"cmd": "move", "mode": "absolute", "angle": 200}) # "move" 명령어를 절대 모드로 처리하는 메서드 호출 (각도가 200으로 설정)
    assert result["result"] == "Error" # 결과가 "Error"인지 확인
