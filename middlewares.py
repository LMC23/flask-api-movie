from flask import request
from functools import wraps
from auth import verify_token

# from token_list import token_list


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        headers = request.headers
        token = headers.get("token")
        if not token:
            return {"error": "Unauthorized", "code": 401}, 401
        try:
            payload = verify_token(token)
            request.payload = payload
            return f(*args, **kwargs)
        except Exception as e:
            if "expired" in str(e):
                return {"error": str(e), "code": 401}, 401
            return {"error": "Unauthorized", "code": 401}, 401

    return decorator


def is_admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        role = request.payload.get("role")
        if role == "ADMIN":
            return f(*args, **kwargs)
        else:
            return {"error": "You are not my master!", "code": 403}, 403

    return decorator
