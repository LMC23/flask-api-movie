from db import Database
from dotenv import dotenv_values

config = dotenv_values(".env")

CONFIG = {
    "HOSTNAME": config.get("DB_HOSTNAME"),
    "DATABASE": config.get("DATABASE"),
    "USERNAME": config.get("DB_USERNAME"),
    "PASSWORD": config.get("DB_PASSWORD"),
    "PORT_ID": config.get("DB_PORT_ID"),
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
