import psycopg2

class User:
    def __init__(self, id=None, username=None, email=None, password=None, is_active=False):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.is_active = is_active

    @classmethod
    def get_by_username(cls, username, conn):
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user_data = cur.fetchone()
        if user_data:
            return cls(*user_data)
        return None

    @classmethod
    def get_by_email(cls, email, conn):
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_data = cur.fetchone()
        if user_data:
            return cls(*user_data)
        return None

    def save(self, conn):
        with conn.cursor() as cur:
            if self.id:
                cur.execute("UPDATE users SET username = %s, email = %s, password = %s, is_active = %s WHERE id = %s",
                            (self.username, self.email, self.password, self.is_active, self.id))
            else:
                cur.execute("INSERT INTO users (username, email, password, is_active) VALUES (%s, %s, %s, %s) RETURNING id",
                            (self.username, self.email, self.password, self.is_active))
                self.id = cur.fetchone()[0]
        conn.commit()
        return self
