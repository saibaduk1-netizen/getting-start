from unittest.mock import patch

from robot.application.run_server import create_server_app, main # TCP 서버 애플리케이션 생성 함수 임포트

def test_create_server_app_returns_server_instance():
    server = create_server_app()
    assert server is not None

@patch("robot.application.run_server.create_server_app") # create_server_app 함수를 패치하여 테스트에서 사용할 수 있도록 함
def test_main_calls_create_server_app(mock_create_server_app):
    mock_server = mock_create_server_app.return_value # 패치된 create_server_app 함수의 반환값을 mock_server로 설정
    main() # main 함수 호출하여 애플리케이션 시작
    mock_server.start.assert_called_once() # mock_server의 start 메서드가 한 번 호출되었는지 확인