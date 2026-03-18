class RobotState: # 로봇 상태 머신 클래스 정의
    def __init__(self): # 초기화 메서드에서 로봇의 상태를 "CLOSED"로 설정
        self.state = "CLOSED" # 로봇의 초기 상태는 "CLOSED"
        self.angle = 0 # 로봇의 초기 각도는 0도로 설정

    def handle_command(self, data): # 명령어를 처리하는 메서드 정의
        cmd = data.get("cmd", "").strip().lower() # 명령어를 소문자로 변환하여 공백 제거
        if cmd == "open": 
            self.state = "OPEN" 
            return {"RESULT": "OK"}
        elif cmd == "close":
            self.state = "CLOSED"
            return {"RESULT": "OK"}
        elif cmd == "move":
            if "angle" not in data:
                return {"RESULT": "ERROR", "MESSAGE": "Missing angle parameter"}
            angle = data["angle"] # 명령어에서 각도 파라미터 추출
            if not isinstance(angle, (int)):
                return {"RESULT": "ERROR", "MESSAGE": "Angle must be a integer"}
            if angle < 0 or angle > 180:
                return {"RESULT": "ERROR", "MESSAGE": "Angle must be between 0 and 180"}
            self.angle = angle # 로봇의 각도 업데이트
            return {"RESULT": "OK", "state": self.state, "angle": self.angle} # 명령어 처리 결과 반환
            
        elif cmd == "status":
            return {"RESULT": "OK", "STATE": self.state, "angle": self.angle} # 로봇의 현재 상태와 각도를 포함한 결과 반환
        else:
            return {"RESULT": "ERROR", "MESSAGE": "Unknown command"}
       
if __name__ == "__main__": # 이 파일이 직접 실행될 때만 아래 코드가 실행되도록 함
    robot = RobotState() # 로봇 상태 머신 인스턴스 생성
    
    while True: # 무한 루프를 사용하여 사용자로부터 명령어를 계속 입력받아 처리
        cmd = input("Enter command: ")
        result = robot.handle_command({"cmd": cmd})
        print("Result:", result)