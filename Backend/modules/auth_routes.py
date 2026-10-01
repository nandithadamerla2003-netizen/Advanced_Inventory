from fastapi import APIRouter, HTTPException, Depends, Request, Form
from database import fetch_one, execute_query
from security import  hash_password, verify_password
from auth import create_access_token, get_current_user
from schemas import Register

router = APIRouter(
    tags=["Authentication"]
)

# Register Route
@router.post("/register")
def register(user: Register):

    # -------------------------
    # Check Email
    # -------------------------

    email_query = """
    SELECT *
    FROM users
    WHERE Email = %s
    """

    existing_email = fetch_one(
        email_query,
        (user.Email,)
    )

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )


    # -------------------------
    # Check Username
    # -------------------------

    username_query = """
    SELECT *
    FROM users
    WHERE username = %s
    """

    existing_username = fetch_one(
        username_query,
        (user.username,)
    )

    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already exists."
        )


    # -------------------------
    # Hash Password
    # -------------------------

    hashed_password = hash_password(
        user.password
    )


    # -------------------------
    # Insert User
    # -------------------------

    insert_query = """
    INSERT INTO users
    (
        full_name,
        Email,
        username,
        password,
        role
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s
    )
    """

    execute_query(

        insert_query,

        (
            user.full_name,
            user.Email,
            user.username,
            hashed_password,
            "User"
        )

    )


    return {

        "message": "Registration Successful."

    }


# Login Route
@router.post("/login")
async def login(
    request: Request,
    username: str = Form(None),
    password: str = Form(None)
):

    content_type = request.headers.get("content-type", "")
    email = None
    pwd = None

    # -------------------------
    # JSON Login
    # -------------------------

    if "application/json" in content_type:
        body = await request.json()
        email = body.get("Email") or body.get("username")
        pwd = body.get("password")

    # Form Login    
    else:
        email = username
        pwd = password

    # Check Login Fields   
    if not email or not pwd:
        raise HTTPException(
            status_code=422,
            detail="Email and password are required."
        )

    query = """
    SELECT *
    FROM users
    WHERE Email=%s OR username=%s
    """

    db_user = fetch_one(
        query,
        (email, email)
    )

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    if not verify_password(
        pwd,
        db_user["password"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    
    # Check Role
    if db_user["role"] not in ["Admin", "User"]:

        raise HTTPException(
            status_code=403,
            detail="Invalid user role"
        )

    # Create JWT
    access_token = create_access_token(
        data={
            "sub": db_user["username"],
            "role": db_user["role"]
        }
    )

    # Return Current User Data
    return {

        "access_token": access_token,

        "token_type": "bearer",

        "user_id": db_user["user_id"],

        "full_name": db_user["full_name"],

        "username": db_user["username"],

        "email": db_user["Email"],

        "role": db_user["role"]

    }

# Current Logged-in User
@router.get("/me")
def current_user(
    user=Depends(get_current_user)
):

    username = user["sub"]


    query = """
    SELECT
        user_id,
        full_name,
        Email,
        username,
        role
    FROM users
    WHERE username = %s
    """


    db_user = fetch_one(
        query,
        (username,)
    )


    if db_user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    return {

        "user_id": db_user["user_id"],

        "full_name": db_user["full_name"],

        "username": db_user["username"],

        "email": db_user["Email"],

        "role": db_user["role"]

    }