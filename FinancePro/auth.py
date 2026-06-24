from database import conn,cursor

def register_user(username,email,password):

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username,email,password)
            VALUES(?,?,?)
            """,
            (username,email,password)
        )

        conn.commit()

        return True

    except:

        return False


def login_user(username,password):

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        AND password=?
        """,
        (username,password)
    )

    return cursor.fetchone()