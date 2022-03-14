import jwt
import datetime

key = "secret"
payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=900),
                'id': "123plm",
                'roles': "admin"
            }
            
encoded = jwt.encode(payload, key, algorithm="HS256")
print(encoded)

decoded = jwt.decode("", key, algorithms="HS256")
print(decoded)