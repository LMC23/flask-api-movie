from database_template import DbTemplate
import bcrypt


class Database(DbTemplate):
    def __init__(self, config):
        super().__init__(config)

    def find_user_by_email(self, email):
        try:
            query_check = """SELECT id, email, password, role FROM users
                            WHERE email = %s"""
            query_values = (email,)
            log_user = self.select_query(query_check, query_values)
            return log_user
        except Exception as e:
            raise e

    def insert_user(self, name, email, password, role="GENERAL"):
        try:
            hashed = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
            hashed = hashed.decode("utf8")

            insert_query = """INSERT INTO  users (name, email, password, role)
                                VALUES (%s, %s, %s, %s)"""
            insert_values = (name, email, hashed, role)
            self.execute_query(insert_query, insert_values)
        except Exception as e:
            raise e
