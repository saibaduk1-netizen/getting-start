from robot.infrastructure.worker import Worker # Worker 클래스 임포트

class DummyQueue: # 테스트용 더미 큐 클래스 정의
    def __init__(self, command): # 초기화 메서드에서 명령어를 저장할 리스트 초기화
        self.commands = command # 받은 명령어를 저장할 변수

    def get(self, timeout=None): # 큐에서 명령어를 가져오는 메서드 정의
        return self.commands # 저장된 명령어 반환   
    
class DummyCommandService: # 테스트용 더미 명령어 서비스 클래스 정의
    def __init__(self): # 초기화 메서드에서 받은 명령어를 저장할 리스트 초기화
        self.received_command = None # 받은 명령어를 저장할 변수

    def process_command(self, command): # 명령어를 처리하는 메서드 정의
        self.received_command = command # 받은 명령어 저장
        return {"result": "OK"} # 처리 결과 반환
    
def test_worker_delegates_command_to_command_service(): # Worker 클래스가 명령어를 CommandService로 위임하는지 테스트하는 함수 정의
    command = {"command": "open"} # 테스트 명령어 정의
    queue = DummyQueue(command) # 더미 큐 인스턴스 생성
    command_service = DummyCommandService() # 더미 명령어 서비스 인스턴스 생성

    worker = Worker(queue, command_service) # Worker 인스턴스 생성
    result = worker.run_once() # Worker의 run_once 메서드 호출

    assert command_service.received_command == command # CommandService가 받은 명령어가 테스트 명령어와 일치하는지 확인
    assert result["result"] == "OK" # 결과가 "OK"인지 확인
    