import psycopg2
import pandas as pd


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

    def select(self, query: str):
        try:
            self.open_connection()
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            df = pd.DataFrame(results, columns=[desc[0] for desc in self.cursor.description])
            print(df)
            
            # return df
        except (Exception, psycopg2.Error) as error:
            print("Ocorreu um erro na conexão do SQL:", error)
        finally:
            self.close_connection()
