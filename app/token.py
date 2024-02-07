"""Create jwt token"""
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "KKUSR85YHGfgfGHETT4T$£Y$%5Gf435Hdhg$%Y43545gWeFW%uJ^%J76K(EE4U45j7j87LKE4RER54565H65"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30

def create_access_token(data: dict):
    """Encoded token"""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
