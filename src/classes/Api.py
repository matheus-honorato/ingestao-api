import requests
from dotenv import load_dotenv
import os

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
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_filmes(self):
        endpoint = "/movie/popular"
        params = {"sort_by": "popularity.desc", "include_adult": "false", "include_video": "false", "page": 1}
        return self.request(endpoint, extra_params=params)

    def get_series(self):
        endpoint = "/tv/popular"
        params = {"sort_by": "popularity.desc", "include_adult": "false", "include_video": "false", "page": 1}
        return self.request(endpoint, extra_params=params)