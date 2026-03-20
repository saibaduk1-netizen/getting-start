from unittest.mock import Mock, patch # Mock과 patch를 unittest.mock에서 임포트하여 테스트에서 객체를 모킹하고 패치할 수 있도록 함

import pytest # pytest 라이브러리 임포트

from robot.interface.tcp_server import TCPServer # TCP 서버 클래스 임포트
from robot.infrastructure.tcp_protocol import ProtocolError # TCP 프로토콜 관련 예외 클래스 임포트
from robot.config.settings import settings # 설정값을 별도의 변수로 임포트

def make_server(): # TCPServer 인스턴스와 모킹된 CommandService를 반환하는 헬퍼 함수 정의
    mock_command_service = Mock()
    return TCPServer(settings.TCP_HOST, settings.TCP_PORT, mock_command_service), mock_command_service


@patch("robot.interface.tcp_server.build_response")     # TCPServer.handle_client 메서드에서 build_response 함수를 패치하여 테스트에서 모킹된 응답을 반환하도록 함
@patch("robot.interface.tcp_server.parse_request")  #  TCPServer.handle_client 메서드에서 parse_request 함수를 패치하여 테스트에서 모킹된 명령어를 반환하도록 함
def test_handle_client_success(mock_parse_request, mock_build_response): # TCPServer.handle_client 메서드가 정상적으로 명령어를 처리하고 응답을 빌드하는지 테스트하는 함수 정의
    server, mock_command_service = make_server()
    client_socket = Mock()

    raw_data = b'{"command": "MOVE"}'
    parsed_command = {"command": "MOVE"}
    built_response = b'{"result": "OK", "message": "Command received"}'

    client_socket.recv.return_value = raw_data
    mock_parse_request.return_value = parsed_command
    mock_build_response.return_value = built_response

    server.handle_client(client_socket)

    client_socket.recv.assert_called_once()
    mock_parse_request.assert_called_once_with(raw_data)
    mock_command_service.submit_command.assert_called_once_with(parsed_command)
    mock_build_response.assert_called_once_with(
        {"result": "OK", "message": "Command received"}
    )
    client_socket.sendall.assert_called_once_with(built_response)


@patch("robot.interface.tcp_server.build_response") # TCPServer.handle_client 메서드에서 build_response 함수를 패치하여 테스트에서 모킹된 응답을 반환하도록 함
@patch("robot.interface.tcp_server.parse_request") # TCPServer.handle_client 메서드에서 parse_request 함수를 패치하여 테스트에서 모킹된 명령어를 반환하도록 함
def test_handle_client_protocol_error(mock_parse_request, mock_build_response): # TCPServer.handle_client 메서드가 프로토콜 오류를 처리하여 적절한 오류 응답을 빌드하는지 테스트하는 함수 정의
    server, mock_command_service = make_server()
    client_socket = Mock()

    raw_data = b"invalid-data"
    error_message = "Invalid JSON"
    built_response = b'{"result": "Error", "message": "Invalid JSON"}'

    client_socket.recv.return_value = raw_data
    mock_parse_request.side_effect = ProtocolError(error_message)
    mock_build_response.return_value = built_response

    server.handle_client(client_socket)

    mock_command_service.submit_command.assert_not_called()
    mock_build_response.assert_called_once_with(
        {"result": "Error", "message": error_message}
    )
    client_socket.sendall.assert_called_once_with(built_response)


@patch("robot.interface.tcp_server.build_response")
@patch("robot.interface.tcp_server.parse_request") 
def test_handle_client_value_error(mock_parse_request, mock_build_response): # TCPServer.handle_client 메서드가 명령어 형식 오류를 처리하여 적절한 오류 응답을 빌드하는지 테스트하는 함수 정의
    server, mock_command_service = make_server()
    client_socket = Mock()

    raw_data = b'{"bad": "command"}'
    error_message = "Unsupported command"
    built_response = b'{"result": "Error", "message": "Unsupported command"}'

    client_socket.recv.return_value = raw_data
    mock_parse_request.side_effect = ValueError(error_message)
    mock_build_response.return_value = built_response

    server.handle_client(client_socket)

    mock_command_service.submit_command.assert_not_called()
    mock_build_response.assert_called_once_with(
        {"result": "Error", "message": error_message}
    )
    client_socket.sendall.assert_called_once_with(built_response)


@patch("robot.interface.tcp_server.build_response") 
@patch("robot.interface.tcp_server.parse_request") 
def test_handle_client_internal_error(mock_parse_request, mock_build_response): # TCPServer.handle_client 메서드가 내부 서버 오류를 처리하여 적절한 오류 응답을 빌드하는지 테스트하는 함수 정의
    server, mock_command_service = make_server()
    client_socket = Mock()

    raw_data = b'{"command": "MOVE"}'
    parsed_command = {"command": "MOVE"}

    client_socket.recv.return_value = raw_data
    mock_parse_request.return_value = parsed_command
    mock_command_service.submit_command.side_effect = RuntimeError("DB down")
    mock_build_response.return_value = b"error-response"

    server.handle_client(client_socket)

    mock_build_response.assert_called_once()
    response_arg = mock_build_response.call_args[0][0]

    assert response_arg["result"] == "Error"
    assert "Internal server error: DB down" == response_arg["message"]

    client_socket.sendall.assert_called_once_with(b"error-response")