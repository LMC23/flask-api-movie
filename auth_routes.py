from flask import Blueprint, request
from auth import check_token, check_admin

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route("/protected", methods=["GET"])
def index():
    token_response = check_token(request)
    if token_response.get("error") != None:
        return token_response, token_response.get("code")
    return {"status": "Ok"}

@auth_blueprint.route("/admin", methods=["GET"])
def admin():
    admin_response = check_admin(request)
    if admin_response.get("error") != None:
        return admin_response, admin_response.get("code")
    return {"status": "Ok"}

#Testing route
@auth_blueprint.route("/", methods=["GET"])
def home():
    return 'Hello World!'