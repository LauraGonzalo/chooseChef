from passlib.hash import bcrypt



def hash_password(password: str) -> str:
    """Convierte una contraseña de texto simple en un hash utilizando bcrypt"""
    return bcrypt.hash(password)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    """Verifica una contraseña de texto simple contra una contraseña con hash."""
    return bcrypt.verify(plain_password, hashed_password)

