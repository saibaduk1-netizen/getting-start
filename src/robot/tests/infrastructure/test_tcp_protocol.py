import pytest
from robot.infrastructure.tcp_protocol import ( ProtocolError, parse_request, build_response)

def test_parse_request_valid(): # parse_request 함수가 유효한 JSON 요청을 올바르게 파싱하는지 테스트하는 함수 정의
    raw_data = b'{"command": "open"}'
    result = parse_request(raw_data)
    assert result == {"command": "open"}

def test_parse_request_empty(): # 빈 요청에 대한 테스트 함수 정의
    with pytest.raises(ProtocolError, match="Empty request"):
        parse_request(b'')  

def test_parse_request_invalid_encoding():
    with pytest.raises(ProtocolError, match="Invalid encoding"):
        parse_request(b'\xff\xfe\x00\x00')

def test_parse_request_invalid_json(): # JSON이 유효하지 않은 경우에 대한 테스트 함수 정의
    with pytest.raises(ProtocolError, match="Invalid JSON"):
        parse_request(b'{"command": "open"')  # Missing closing brace

def test_parse_request_non_object(): # JSON이 객체가 아닌 경우에 대한 테스트 함수 정의
    with pytest.raises(ProtocolError, match="Request JSON must be an object"):
        parse_request(b'["command", "open"]')  # JSON array instead of object

def test_build_response_valid(): # build_response 함수가 유효한 딕셔너리를 받아 올바른 JSON 응답을 생성하는지 테스트하는 함수 정의
    payload = {"result": "OK", "message": "Success"}
    result = build_response(payload)
    assert isinstance(result, bytes)
    assert result == b'{"result": "OK", "message": "Success"}'

def test_build_response_non_dict(): # build_response 함수가 딕셔너리가 아닌 입력에 대해 ProtocolError를 발생시키는지 테스트하는 함수 정의
    with pytest.raises(ProtocolError, match="Response payload must be a dict"):
        build_response(["result", "OK"])  # List instead of dict