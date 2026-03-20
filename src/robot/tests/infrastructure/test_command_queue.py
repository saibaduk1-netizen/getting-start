from robot.infrastructure.command_queue import CommandQueue # CommandQueue 클래스 임포트

def test_command_queue_put_and_get(): # CommandQueue 클래스의 put과 get 메서드를 테스트하는 함수 정의
    command_queue = CommandQueue() # CommandQueue 인스턴스 생성
    command = {"command": "open"} # 테스트 명령어 정의

    command_queue.put(command) # 명령어 큐에 명령어 추가
    result = command_queue.get() # 명령어 큐에서 명령어 가져오기
    assert result == command # 가져온 명령어가 테스트 명령어와 일치하는지 확인
    