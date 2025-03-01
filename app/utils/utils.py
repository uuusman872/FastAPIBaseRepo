from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from config import Config
import uuid

password_context = CryptContext(
    schemes=['bcrypt']
)
ALGORITHM_EXPIRY_TIME = 3600

def generate_passwd_hash(password: str) -> str:
    hash = password_context.hash(password)
    return hash

def verify_password(password: str, hash_password) -> str:
    return password_context.verify(password, hash_password)


def generate_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {
        "user": user_data,
        "exp": datetime.now() + expiry if expiry else datetime.now() + timedelta(seconds=ALGORITHM_EXPIRY_TIME),
        "jti": str(uuid.uuid4()),  # Convert UUID to string
        "refresh": refresh
    }
    
    token = jwt.encode(payload=payload, key=Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return token


def decode_token(token: str) -> str:
    try:
        token_data = jwt.decode(jwt=token, key=Config.JWT_SECRET_KEY, algorithms=Config.JWT_ALGORITHM)
        return token_data
    except Exception as e:
        return None

