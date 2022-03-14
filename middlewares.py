from flask import request
from functools import wraps

from token_list import token_list

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        headers = request.headers
        token = headers.get("api-key")
        if not token:
            return {"error": "Unauthorized", "code": 401}
        if token not in [item.get("token") for item in token_list]:
            return {"error": "Unauthorized", "code": 401}
        
        return f(*args, **kwargs)
    
    return decorator

