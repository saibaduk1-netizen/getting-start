class RobotState: # 로봇 상태 머신 클래스 정의
    def __init__(self): # 초기화 메서드에서 로봇의 상태를 "CLOSED"로 설정
        self.state = "CLOSED" # 로봇의 초기 상태는 "CLOSED"
        self.angle = 0 # 로봇의 초기 각도는 0도로 설정

    def handle_command(self, data): # 명령어를 처리하는 메서드 정의
        cmd = data.get("cmd", "") # 명령어를 데이터에서 추출, 기본값은 빈 문자열
        if not cmd: # 명령어가 없는 경우 오류 메시지 반환
            return {"result": "Error", "Message": "Missing command"}
        cmd = cmd.strip().lower() # 명령어를 소문자로 변환하여 공백 제거

        if cmd == "open": 
            self.state = "OPEN" 
            return {"result": "OK", "state": self.state, "angle": self.angle}
        elif cmd == "close":
            self.state = "CLOSED"
            return {"result": "OK", "state": self.state, "angle": self.angle}
        elif cmd == "move":
            mode = data.get("mode", "absolute").strip().lower() # 이동 모드를 데이터에서 추출, 기본값은 "absolute"
            if mode == "absolute":
                if "angle" not in data:
                    return {"result": "Error", "message": "Missing angle parameter"}
                angle = data["angle"] # 명령어에서 각도 파라미터 추출
                if not isinstance(angle, (int)):
                    return {"result": "Error", "message": "Angle must be a integer"}
                if angle < 0 or angle > 180:
                    return {"result": "Error", "message": "Angle must be between 0 and 180"}
                self.angle = angle # 로봇의 각도 업데이트
                return {"result": "OK", "state": self.state, "angle": self.angle}
            elif mode == "relative":
                    if "delta" not in data:
                        return {"result": "Error", "message": "Missing delta parameter"}
                    delta = data["delta"] # 명령어에서 각도 변화량 파라미터 추출
                    if not isinstance(delta, (int)):
                        return {"result": "Error", "message": "Delta must be a integer"}
                    new_angle = self.angle + delta # 새로운 각도 계산
                    if new_angle < 0 or new_angle > 180:
                        return {"result": "Error", "message": "Resulting angle must be between 0 and 180"}
                    self.angle = new_angle # 로봇의 각도 업데이트
                    return {"result": "OK", "state": self.state, "angle": self.angle}
            else:
                return {"result": "Error", "message": "Invalid move mode"}

        elif cmd == "status":
            return {"result": "OK", "state": self.state, "angle": self.angle}
        else:
            return {"result": "Error", "message": "Unknown command"}
       
if __name__ == "__main__": # 이 파일이 직접 실행될 때만 아래 코드가 실행되도록 함
    robot = RobotState() # 로봇 상태 머신 인스턴스 생성
    
    while True: # 무한 루프를 사용하여 사용자로부터 명령어를 계속 입력받아 처리
        cmd = input("Enter command: ")
        result = robot.handle_command({"cmd": cmd})
        print("Result:", result)