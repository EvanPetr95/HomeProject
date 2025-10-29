from passlib.context import CryptContext

PWD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"])
