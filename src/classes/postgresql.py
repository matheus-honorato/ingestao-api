import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2.extras as extras
import logging

load_dotenv()


class Postgresql:
    """
    A classe é responsável por operações com o banco de dados PostgreSQL: Gerenciamento de conexões,
    execução de consultas e inserção de dados.

    Esta classe fornece métodos para:
    - Estabelecer e gerenciar conexões com o banco de dados
    - Executar consultas SELECT e retornar resultados como DataFrames do pandas
    - Inserir dados de DataFrames em tabelas
    - Executar operações DDL (CREATE e DROP de tabelas)

    Attributes:
        __connection_string (str): String de conexão construída a partir de variáveis de ambiente
    """

    def __init__(self):
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")
        self.__connection_string = f"host={host} port={port} dbname={database} user={user} password={password}"

    def open_connection(self) -> None:
        try:
            conn = psycopg2.connect(self.__connection_string)
            self.conn = conn
            self.cursor = conn.cursor()
        except psycopg2.OperationalError as e:
            raise logging.error(f"Falha ao conectar ao banco de dados: {str(e)}")

    def close_connection(self):
        """Fecha o cursor e a conexão com o banco de dados se eles existirem."""
        self.cursor.close()
        self.conn.close()

    def select(self, query: str) -> pd.DataFrame:
        """
        Executa uma consulta SQL SELECT e retorna os resultados como um DataFrame.

        Args:
            query (str): Consulta SQL a ser executada

        Returns:
            pd.DataFrame: DataFrame contendo os resultados da consulta

        Raises:
            psycopg2.Error: Para erros específicos do PostgreSQL
        """
        try:
            self.open_connection()
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            df = pd.DataFrame(results, columns=[desc[0] for desc in self.cursor.description])
            return df

        except (Exception, psycopg2.Error) as error:
            logging.error("Ocorreu um erro na conexão do SQL:", error) 
        finally:
            self.close_connection()

    def insert(self, df, name_table) -> None:
        """
        Insere os dados de um DataFrame do Pandas em uma tabela do banco de dados PostgreSQL.

        Args:
            df: DataFrame contendo os dados a serem inseridos no banco.
            name_table: Nome da tabela onde os dados serão inseridos.
        """
        tuples = [tuple(x) for x in df.to_numpy()]
        colums = ','.join(list(df.columns))
        try:
            self.open_connection()
            query = "INSERT INTO %s(%s) VALUES %%s" % (name_table, colums)
            extras.execute_values(self.cursor, query, tuples)
            self.conn.commit()
            logging.info("Dados inserido com sucesso.")
        except (Exception, psycopg2.Error) as error:
            self.conn.rollback()
            logging.error("Ocorreu um erro na conexão do SQL:", error)
        finally:
            self.close_connection()

    def create_or_delete_table(self, query: str) -> None:
        """
        Executa uma operação DDL (Data Definition Language) para criar ou excluir tabelas no PostgreSQL.

        Esta função é destinada especificamente para comandos CREATE TABLE e DROP TABLE.
        Gerencia automaticamente a transação, fazendo commit em caso de sucesso e rollback em caso de erro.

        Args:
            query (str): Comando SQL DDL completo para criação ou exclusão de tabela.
        Raises:
            psycopg2.ProgrammingError: Se houver erro de sintaxe no SQL
            psycopg2.Error: Captura de erros genéricos
        """
        try:
            self.open_connection()
            self.cursor.execute(query)
            self.conn.commit()
            logging.info("Query create/delete executada com sucesso")
        except psycopg2.ProgrammingError as e:
            self.conn.rollback()
            raise logging.error(f"Erro de sintaxe na query: {str(e)}")

        except (Exception, psycopg2.Error) as e:
            self.conn.rollback()
            logging.error("Ocorreu um erro na conexão do SQL:", e)

        finally:
            self.close_connection()
