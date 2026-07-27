from passlib.context import CryptContext

# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Hash Password
def hash_password(password: str) -> str:
    """
    Convert a plain-text password into a hashed password.
    """
    return pwd_context.hash(password)

# Verify Password
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Compare the entered password with the stored hashed password.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password
    )