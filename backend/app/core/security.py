from datetime import timedelta
import bcrypt
from jose import jwt
from app.core.config import settings
from app.db.models.users import now, uid

ALGORITHM = "HS256"

def create_token(user, kind="access", minutes=15, token_id=None):
    return jwt.encode({"sub": user.id, "role": user.role.value, "type": kind,
                       "ver": user.token_version, "jti": token_id or uid(),
                       "exp": now() + timedelta(minutes=minutes)},
                      settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token, kind):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    if payload.get("type") != kind:
        raise ValueError("Invalid token type")
    return payload

def get_password_hash(password):
    return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode()

def verify_password(password, encoded):
    try:
        return bcrypt.checkpw(password.encode("utf8"), encoded.encode())
    except (ValueError, TypeError):
        return False
