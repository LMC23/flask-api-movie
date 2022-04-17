from auth import create_token, verify_token


def test_create_token():
    payload = {"id": 1}
    result_token = create_token(payload)
    assert isinstance(result_token, str) is True
    assert len(result_token) > 0


def test_verify_token():
    payload = {"id": 1}
    token = create_token(payload)
    result_decoded = verify_token(token)
    assert result_decoded.get("id") == payload.get("id")
