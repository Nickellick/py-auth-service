from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_hash(sensitive_info: str) -> str:
    return pwd_context.hash(sensitive_info)

def verify_hash(sensitive_info: str, hash_: str) -> bool:
    return pwd_context.verify(sensitive_info, hash_)