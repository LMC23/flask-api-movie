from token_list import token_list

def check_token(request):
    headers = request.headers
    token = headers.get("api-key")
    if not token:
        return {"error": "Unauthorized", "code": 401}
    if token not in [item.get("token") for item in token_list]:
        return {"error": "Unauthorized", "code": 401}
    
    return {"error": None, "code": 200}
    