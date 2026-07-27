from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import fetch_one
from security import verify_password
from auth import create_access_token, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends()):

    query = """
    SELECT *
    FROM users
    WHERE username=%s
    """

    db_user = fetch_one(
        query,
        (user.username,)
    )

    if db_user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        user.password,
        db_user["password"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={
            "sub": db_user["username"],
            "role": db_user["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Current Logged-in User
@router.get("/me")
def current_user(
    user=Depends(get_current_user)
):

    return {
        "username": user["sub"],
        "role": user["role"]
    }