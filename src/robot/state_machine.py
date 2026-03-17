class RobotState: # A simple state machine for a robot that can be OPEN or CLOSED
    def __init__(self):
        self.state = "CLOSED"

    def handle_command(self, cmd):
        cmd = cmd.strip().lower()
        if cmd == "open":
            self.state = "OPEN" 
        elif cmd == "close":
            self.state = "CLOSED"
        elif cmd == "status":
            return self.state
        else:
            return "ERROR"
        return "OK"
"""
주석을 이렇게 다는구나.
"""
# 한줄 주석은 이렇게
if __name__ == "__main__": 
    robot = RobotState()
    
    while True:
        cmd = input("Enter command: ")
        result = robot.handle_command(cmd)
        print("Result:", result)