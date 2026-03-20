from unittest.mock import patch

from robot.application.run_client import create_client_app, main # TCP 클라이언트 애플리케이션 생성 함수 임포트

def test_create_client_app_returns_client_instance():
    client = create_client_app()
    assert client is not None

@patch("builtins.input", side_effect=["exit"]) # input 함수를 패치하여 "exit" 입력을 시뮬레이션
@patch("robot.application.run_client.create_client_app") # create_client_app 함수를 패치하여 테스트에서 사용할 수 있도록 함
def test_main_exits_on_exit(mock_create_client_app, mock_input):
    mock_client = mock_create_client_app.return_value
    main()
    mock_client.send.assert_not_called() # send_command 메서드가 호출되지 않았는지 확인

@patch("builtins.print") # print 함수를 패치하여 출력 내용을 테스트에서 확인할 수 있도록 함
@patch("builtins.input", side_effect=["MOVE", "exit"]) # input 함수를 패치하여 "MOVE"와 "exit" 입력을 시뮬레이션
@patch("robot.application.run_client.create_client_app") # create_client_app 함수를 패치
def test_main_sends_command_and_prints_response(mock_create_client_app, mock_input, mock_print):
    mock_client = mock_create_client_app.return_value
    mock_client.send_command.return_value = '{"status": "ok"}' # send_command 메서드의 반환값을 "OK"로 설정
    main()
    mock_client.send_command.assert_called_once_with("MOVE") # send_command 메서드가 "MOVE" 명령어로 한 번 호출되었는지 확인
    first_printed = mock_print.call_args_list[0].args[0]
    assert "Response from server:" in first_printed
    assert "status" in first_printed
    assert "ok" in first_printed