import jwt
from datetime import timedelta, datetime

secret_key = 'long bite str'

def auth_user(id, role):
    encoded_jwt = jwt.encode({
        "user_id": id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours = 3)
        }, secret_key, algorithm="HS256")
    return encoded_jwt

def check_auth(token):
    if token == None:
        return False
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False
    return decoded

def path_handler(role, allowed):
    if allowed == "*":
        return True
    elif allowed == role:
        return True
    elif role in allowed:
        return True
    else:
        return False