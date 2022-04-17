from flask import Blueprint, request
from auth import create_token
from db import Database
import psycopg2.errorcodes
import bcrypt
import logging

from middlewares import token_required, is_admin

auth_blueprint = Blueprint("auth_blueprint", __name__)

logging.basicConfig(filename="app.log", filemode="a", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


CONFIG = {
    "HOSTNAME": "localhost",
    "DATABASE": "flask_database",
    "USERNAME": "postgres",
    "PASSWORD": "password",
    "PORT_ID": 5432,
}

db = Database(CONFIG)


@auth_blueprint.route("/protected", methods=["GET"])
@token_required
def index():
    print(request.payload)
    return {"status": "Ok"}


@auth_blueprint.route("/admin", methods=["GET"])
@token_required
@is_admin
def admin():
    return {"status": "Ok"}


@auth_blueprint.route("/register", methods=["POST"])
def create_user():
    try:
        user_input = request.json
        name = user_input.get("name")
        email = user_input.get("email")
        password = user_input.get("password")

        db.insert_user(name, email, password)
        logger.info(f"User {name} has been successfully created.")
        return {"message": "User created successfully."}

    except psycopg2.IntegrityError as e:
        if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
            logger.error(f"An error has occurred {str(e)}")
            return {"error": "Values must be unique."}

    except Exception as e:
        error = str(e)
        logger.error(f"User could not be created due to {error}")


@auth_blueprint.route("/login", methods=["POST"])
def login():
    try:
        credentials = request.json
        password = credentials.get("password")
        email = credentials.get("email")
        if email is None or password is None:
            return {"message": "Please provide email and password."}

        log_user = db.find_user_by_email(email)

        if log_user is None:
            return {"message": "Invalid credentials."}
        if bcrypt.checkpw(password.encode("utf8"), log_user["password"].encode("utf8")):
            payload = {"id": log_user.get("id"), "role": log_user.get("role")}
            token = create_token(payload)
            return {"token": token}
        else:
            return {"message": "Invalid credentials."}
    except Exception as e:
        error = str(e)
        logger.error(f"Could not login due to {error}")
        return {"error": error}


@auth_blueprint.route("/create_admin", methods=["POST"])
@token_required
@is_admin
def create_admin():
    try:
        user_input = request.json
        name = user_input.get("name")
        email = user_input.get("email")
        password = user_input.get("password")
        role = "ADMIN"

        db.insert_user(name, email, password, role)
        logger.info(f"Admin {name} created successfully.")
        return {"message": "Admin created successfully."}

    except psycopg2.IntegrityError as e:
        if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
            return {"error": "Values must be unique."}


# Testing route
@auth_blueprint.route("/", methods=["GET"])
def home():
    return "Hello World!"
