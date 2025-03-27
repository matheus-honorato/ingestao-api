import requests
from dotenv import load_dotenv
import os
import logging

load_dotenv()  # Identifica as variaveis de ambiente criada em .env e conseguimos utilizar no código


class Api:
    base_url = "https://api.themoviedb.org/3"

    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "Authorization": os.getenv('API_KEY', None)
            }
        self.params = {
            "language": "pt-BR"
        }

    def request(self, endpoint, extra_params=None):
        url = f"{self.base_url}{endpoint}"
        params = self.params.copy()
        if extra_params:
            params.update(extra_params)
        try:
            logging.info(f"Iniciando requisição para o endpoint: {url}")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição {url}: {e}")
            return None

    def get_filmes_populares_tmbd(self):
        time_window = "day"
        endpoint = f"/trending/movie/{time_window}" 
        return self.request(endpoint)

    def get_series_populares_tmbd(self):
        time_window = "day" 
        endpoint = f"/trending/tv/{time_window}"
        return self.request(endpoint)
  