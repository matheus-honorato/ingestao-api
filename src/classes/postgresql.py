import psycopg2


class Postgresql:

    def __init__(self, user: str, host: str, port: int, password: str, database: str):
        self.__connection_string = f"host={host} port={port} dbname={database} user={user} password={password}"

    def open_connection(self):
        conn = psycopg2.connect(self.__connection_string)
        self.conn = conn
        self.cursor = conn.cursor()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()


