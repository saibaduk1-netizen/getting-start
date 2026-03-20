from robot.domain.robot_state import RobotState # 로봇 상태 클래스 임포트

class StateMachine:
    def __init__(self) -> None: # StateMachine 클래스의 초기화 메서드 정의, 로봇 상태를 관리하는 RobotState 인스턴스를 생성하여 초기화
        self.state = RobotState() # StateMachine 클래스의 인스턴스가 생성될 때 RobotState 인스턴스를 초기화하여 상태를 관리

    def handle_command(self, robot_state: RobotState, command: dict) -> dict: # 명령어를 처리하는 메서드 정의, 입력은 딕셔너리 형태의 명령어, 출력도 딕셔너리 형태의 결과
        command = command.get("command", "").strip().lower() # 명령어에서 "command" 키의 값을 추출하여 소문자로 변환하고 공백 제거, 기본값은 빈 문자열
        if not command: 
            return {"result": "Error", "message": "Missing command"}
        
        if command == "open": 
            robot_state.gripper_state = "OPEN" 
            return {"result": "OK", "state": robot_state.gripper_state, "angle": robot_state.angle} # "open" 명령어 처리, 로봇의 그리퍼 상태를 "OPEN"으로 변경하고 처리 결과 반환
        elif command == "close": 
            robot_state.gripper_state = "CLOSED" 
            return {"result": "OK", "state": robot_state.gripper_state, "angle": robot_state.angle} # "close" 명령어 처리, 로봇의 그리퍼 상태를 "CLOSED"로 변경하고 처리 결과 반환
        elif command == "move": 
            return self._handle_move(robot_state, command)
        elif command == "status":
            return self._ok_response(robot_state) # "status" 명령어 처리, 로봇의 현재 상태와 각도를 포함하여 처리 결과 반환
        else:
            return {"result": "Error", "message": "Unknown command"} # 유효하지 않은 명령어에 대한 오류 메시지 반환

    def _handle_move(self, robot_state: RobotState, command: dict) -> dict: # "move" 명령어를 처리하는 별도의 메서드 정의, 이동 모드와 각도 파라미터를 처리하여 로봇의 각도를 업데이트하고 결과 반환
        mode = command.get("mode", "absolute").strip().lower() # 이동 모드를 명령어에서 추출, 기본값은 "absolute", 소문자로 변환하여 공백 제거
        if not isinstance(mode, str):
            return {"result": "Error", "message": "Mode must be a string"}
        if mode == "absolute":
            if "angle" not in command:
                return {"result": "Error", "message": "Missing angle parameter"}
            angle = command["angle"] # 명령어에서 각도 파라미터 추출
            if not isinstance(angle, (int)):
                return {"result": "Error", "message": "Angle must be a integer"}
            if angle < 0 or angle > 180:
                return {"result": "Error", "message": "Angle must be between 0 and 180"}
            robot_state.angle = angle # 로봇의 각도 업데이트
            return self._ok_response(robot_state) # 처리 결과 반환
        elif mode == "relative":
            if "delta" not in command:
                return {"result": "Error", "message": "Missing delta parameter"}
            delta = command["delta"] # 명령어에서 각도 변화량 파라미터 추출
            if not isinstance(delta, (int)):
                return {"result": "Error", "message": "Delta must be a integer"}
            new_angle = robot_state.angle + delta # 새로운 각도 계산
            if new_angle < 0 or new_angle > 180:
                return {"result": "Error", "message": "Resulting angle must be between 0 and 180"}
            robot_state.angle = new_angle # 로봇의 각도 업데이트
            return self._ok_response(robot_state) # 처리 결과 반환
        else:
            return {"result": "Error", "message": "Invalid move mode"} # 유효하지 않은 이동 모드에 대한 오류 메시지 반환
        
    def _ok_response(self, robot_state: RobotState) -> dict: # 처리 결과가 성공인 경우의 응답을 생성하는 별도의 메서드 정의, 로봇의 현재 상태와 각도를 포함하여 반환
        return {"result": "OK", "state": robot_state.gripper_state, "angle": robot_state.angle}