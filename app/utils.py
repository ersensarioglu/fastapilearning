"""Various local utilities"""
import logging
from passlib.context import CryptContext

logging.getLogger('passlib').setLevel(logging.ERROR)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def my_hash(password: str):
    """Local hashing function"""
    return pwd_context.hash(password)

def verify_login(plain_password, hashed_password):
    """Verify user password"""
    return pwd_context.verify(plain_password, hashed_password)
