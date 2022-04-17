import psycopg2
import psycopg2.extras


class DbTemplate:
    def __init__(self, config):
        self.hostname = config.get("HOSTNAME")
        self.database = config.get("DATABASE")
        self.username = config.get("USERNAME")
        self.password = config.get("PASSWORD")
        self.port_id = config.get("PORT_ID")
        self.conn = None

    def open_connection(self):
        try:
            self.conn = psycopg2.connect(
                host=self.hostname,
                dbname=self.database,
                user=self.username,
                password=self.password,
                port=self.port_id,
            )
        except psycopg2.DatabaseError as error:
            raise error

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def select_query(self, query, values=tuple()):
        CUR = None
        try:
            self.open_connection()
            if self.conn is None:
                raise ValueError("Could not execute query {query}. Connection could not be opened.")
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as CUR:
                CUR.execute(query, values)
                records = []
                for record in CUR.fetchall():
                    records.append(record)
                if len(records) == 1:
                    return records[0]
                if len(records) == 0:
                    return None
                return records
        except psycopg2.DatabaseError as error:
            raise error
        finally:
            self.close_connection()
            if CUR is not None:
                CUR.close()

    def execute_query(self, query, values=tuple()):
        CUR = None
        try:
            self.open_connection()
            if self.conn is None:
                raise ValueError(f"Could not execute query {query}. Connection could not be opened.")
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as CUR:
                CUR.execute(query, values)
                rows_affected = f"{CUR.rowcount} rows affected."
                self.conn.commit()
                return rows_affected
        except psycopg2.DatabaseError as error:
            raise error
        finally:
            self.close_connection()
            if CUR is not None:
                CUR.close()
