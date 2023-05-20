from sqlite3 import Connection


def init_db(path="db.sqlite3"):
    sql = """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username VARCHAR (255) NOT NULL,
        email VARCHAR (255) UNIQUE,
        phone INTEGER
        );
    """
    connection = Connection(path)
    connection.execute(sql)
    connection.close()


if __name__ == "__main__":
    init_db()
