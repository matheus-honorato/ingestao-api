from classes.api import Api
from classes.manipuladiretorio import ManipulaDiretorio
from classes.postgresql import Postgresql
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(asctime)s -  %(message)s", filename='/code/logs_pipeline.log')
    
    logging.info("Iniciando pipeline de dados...")
    api = Api()
    filmes = api.get_filmes_populares_tmbd()

    ManipulaDiretorio = ManipulaDiretorio("downloads", filmes)
    create_directory = ManipulaDiretorio.create_directory()
    generate_file_name = ManipulaDiretorio.generate_file_name()
    df = ManipulaDiretorio.json_to_csv()
    logging.info("Iniciando conexão com o banco de dados")
    postgres = Postgresql()

    query = """
    CREATE TABLE IF NOT EXISTS dados_api (
        data_extracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        adult BOOLEAN,
        backdrop_path VARCHAR(255),
        genre_ids TEXT, 
        id INT PRIMARY KEY,
        original_language VARCHAR(10),
        original_title VARCHAR(255),
        overview TEXT,
        popularity FLOAT,
        poster_path VARCHAR(255),
        media_type VARCHAR(255),
        release_date DATE,
        title VARCHAR(255),
        video BOOLEAN,
        vote_average FLOAT,
        vote_count INT
    );
    """
    create_table = postgres.create_or_delete_table(query)
    insert_data = postgres.insert(df, "dados_api")
    select_data = postgres.select("SELECT * FROM dados_api")
    print(select_data)
    logging.info("Pipeline de dados finalizado.")
