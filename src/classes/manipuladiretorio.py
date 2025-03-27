import pandas as pd
import os
import datetime
import logging
from typing import Dict, Any


class ManipulaDiretorio:
    """
    Classe para manipulação de arquivos e diretórios.

    Attributes:
        path_download (str): Caminho onde os arquivos serão salvos.
        data_json (dict): Dados em formato JSON a serem convertidos.
        name_file (str | None): Nome do arquivo gerado (opcional).
    """

    def __init__(self, path_download: str, data_json: Dict[str, Any]):
        self.path_download = path_download
        self.data_json = data_json
        self.name_file = None
    
    def create_directory(self) -> None:
        """
        Responsável pela criação do diretório onde será armazenado os arquivos csv.
        
        Raises:
            OSError: Se ocorrer um erro ao criar o diretório.
        """
        try:
            if not os.path.exists(self.path_download):
                os.makedirs(self.path_download)
                logging.info(f"Criando diretório {self.path_download}")
            else:
                logging.warning(f"Diretório {self.path_download} já existe...pulando")
        except OSError as e:
            logging.error(f"Erro ao criar diretório {self.path_download}: {e}")
            raise

    def generate_file_name(self) -> None:
        """
        Gera um nome de arquivo único com base no timestamp atual.
        
        O nome gerado é armazenado no atributo name_file no formato 'data_YYYY-MM-DD_HH-MM.csv'.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        self.name_file = f"data_{timestamp}.csv"
        logging.info(f"Nome do arquivo gerado {self.name_file}")

    def json_to_csv(self) -> pd.DataFrame:
        """
        Converte os dados JSON para CSV e salva no diretório especificado.
        
        Returns:
            pd.DataFrame: DataFrame pandas criado a partir dos dados JSON.
            
        Raises:
            ValueError: Se data_json não contiver a chave 'results' ou se name_file não foi gerado.
            OSError: Se ocorrer um erro ao salvar o arquivo.
        """
        try:
            if not self.name_file:
                raise ValueError(logging.error("Nome do arquivo não foi gerado. Execute generate_file_name() primeiro"))
            
            if "results" not in self.data_json:
                raise ValueError(logging.error("Chave 'results' não encontrada em data_json"))
            
            logging.info(f"Iniciando conversão para o arquivo: {self.name_file}")

            path_file = os.path.join(self.path_download, self.name_file)
            results_data = self.data_json.get("results")
            df = pd.DataFrame(results_data)
            df.to_csv(path_file, encoding='utf-8', index=False)
            logging.info(f"Arquivo CSV gerado com sucesso: {path_file}")
            return df
        except Exception as e:
            logging.exception(f"Falha crítica ao converter JSON para CSV: {str(e)}")
            raise
