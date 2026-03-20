from queue import Empty # Empty 예외 클래스 임포트
 
class Worker: # Worker 클래스 정의
    def __init__(self, cmd_queue, cmd_service):
        self.cmd_queue = cmd_queue
        self.cmd_service = cmd_service
        self._running = False
        
    def run_once(self):
        cmd = self.cmd_queue.get(timeout=1) # 명령어 큐에서 명령어를 가져옴
        return self.cmd_service.process_command(cmd) # CommandService의 process_command 메서드를 호출하여 명령어를 처리하고 결과를 반환
    
    def run_forever(self):
        self._running = True
        while self._running:
            try:
                cmd = self.cmd_queue.get(timeout=0.1) # 명령어 큐에서 명령어를 가져옴, 타임아웃을 설정하여 큐가 비어있을 때 예외가 발생하도록 함
            except Empty: # 큐가 비어있을 때 발생하는 예외 처리
                continue # 큐가 비어있으면 계속해서 명령어를 기다림 

            self.cmd_service.process_command(cmd) # CommandService의 process_command 메서드를 호출하여 명령어를 처리

    def stop(self):
        self._running = False # run_forever 루프를 종료하기 위해 _running 플래그를 False로 설정
        