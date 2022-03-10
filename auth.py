from token_list import token_list

def check_token(request):
    headers = request.headers
    token = headers.get("api-key")
    if not token:
        return {"error": "Unauthorized", "code": 401}
    if token not in [item.get("token") for item in token_list]:
        return {"error": "Unauthorized", "code": 401}
    
    return {"error": None, "code": 200}

def check_admin(request):
    headers = request.headers
    token = headers.get("api-key")
    if not token:
        return {"error": "Unauthorized", "code": 401}
    if token not in [item.get("token") for item in token_list]:
        return {"error": "Unauthorized", "code": 401}
    has_access = False
    for item in token_list:
        access_level = item.get("admin")
        if token == item.get("token"):
            has_access = access_level
            break
    if has_access is False:
        return {"error": "Unauthorized", "code": 403}
    
    return {"error": None, "code": 200}