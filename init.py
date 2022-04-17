from db import Database

CONFIG = {
    "HOSTNAME": "localhost",
    "DATABASE": "flask_database",
    "USERNAME": "postgres",
    "PASSWORD": "password",
    "PORT_ID": 5432,
}

try:
    db = Database(CONFIG)
    drop_query = "DROP TABLE IF EXISTS users"
    drop_table = db.execute_query(drop_query)

    table_template = """ CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name varchar(40) NOT NULL,
                email varchar(100) UNIQUE NOT NULL,
                password varchar(200) NOT NULL,
                role varchar(100) NOT NULL
            )
            """
    create_table = db.execute_query(table_template)
    print(create_table)
except Exception as error:
    print(error)
