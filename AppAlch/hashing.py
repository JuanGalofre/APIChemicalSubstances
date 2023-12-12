from passlib.context import CryptContext
import bcrypt
pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash(password):
    return pwd_context.hash(password)
def verifyPassword(user_password,stored_password):
    return pwd_context.verify(user_password,stored_password)