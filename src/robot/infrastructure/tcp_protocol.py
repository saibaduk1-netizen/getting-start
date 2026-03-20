import json

class ProtocolError(Exception):
    pass

def parse_request(raw_data: bytes) -> dict:
    if not raw_data:
        raise ProtocolError("Empty request")
    
    try:
        text = raw_data.decode("utf-8").strip()
    except UnicodeDecodeError as exc:
        raise ProtocolError("Invalid encoding") from exc
    
    if not text:
        raise ProtocolError("Empty command")
    
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ProtocolError("Invalid JSON") from exc
    
    if not isinstance(payload, dict):
        raise ProtocolError("Request JSON must be an object")
    
    return payload

def build_response(payload: dict) -> bytes:
    if not isinstance(payload, dict):
        raise ProtocolError("Response payload must be a dict")
    
    text = json.dumps(payload)
    return text.encode("utf-8")