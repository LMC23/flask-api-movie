import jwt
import datetime
from dotenv import dotenv_values

config = dotenv_values(".env")


def create_token(payload):
    try:
        key = config.get("JWT_SECRET")
        if key is None:
            raise ValueError("Could not get JWT secret.")
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=900)

        encoded = jwt.encode(payload, key, algorithm="HS256")

        return encoded
    except Exception as e:
        raise e


def verify_token(token):
    try:
        key = config.get("JWT_SECRET")
        if key is None:
            raise ValueError("Could not get JWT secret.")
        decoded = jwt.decode(token, key, algorithms=["HS256"])
        return decoded
    except Exception as e:
        raise e
