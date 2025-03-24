import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np 
import psycopg2.extras as extras 


load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST") 
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")


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
            return df

        except (Exception, psycopg2.Error) as error:
            print("Ocorreu um erro na conexão do SQL:", error)
        finally:
            self.close_connection()

    def insert(self, df, name_table):
        tuples = [tuple(x) for x in df.to_numpy()] 
        colums = ','.join(list(df.columns)) 
        try:
            self.open_connection()
            query = "INSERT INTO %s(%s) VALUES %%s" % (name_table, colums) 
            extras.execute_values(self.cursor, query, tuples) 
            self.conn.commit()
            print("Dados inserido com sucesso...")
        except (Exception, psycopg2.Error) as error:
            self.conn.rollback()
            print("Ocorreu um erro na conexão do SQL:", error)
        finally:
            self.close_connection()


