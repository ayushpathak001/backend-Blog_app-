from passlib.context import CryptContext

password_hash = CryptContext(schemes=["bcrypt"] ,deprecated = "auto")

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)
