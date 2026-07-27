from config import ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_ROLE

from security import hash_password
from database import fetch_one, execute_query


def create_admin():

    # Check if admin already exists
    query = """
    SELECT *
    FROM users
    WHERE username = %s
    """

    user = fetch_one(
        query,
        (ADMIN_USERNAME,)
    )

    if user:

        print("Admin user already exists.")
        return

    # Hash the password
    hashed_password = hash_password(
        ADMIN_PASSWORD
    )

    # Insert admin user
    insert_query = """
    INSERT INTO users
    (
        username,
        password,
        role
    )
    VALUES
    (
        %s,
        %s,
        %s
    )
    """

    execute_query(
        insert_query,
        (
            ADMIN_USERNAME,
            hashed_password,
            ADMIN_ROLE
        )
    )

    print("Admin user created successfully.")


if __name__ == "__main__":
    create_admin()