import requests
import os
import logging


class Api:
    """
    Classe que interage com a API do TMDB para acessar dados de filmes e séries.

    Esta classe fornece métodos para fazer requisições à API do TMDB e retornar
    informações sobre filmes populares ou séries populares. 

    """
    base_url = "https://api.themoviedb.org/3"

    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "Authorization": os.getenv('API_KEY', None)
            }
        self.params = {
            "language": "pt-BR"
        }

    def request(self, endpoint, extra_params=None) -> dict:
        """
        Faz uma requisição GET para o endpoint especificado.

        Esse método constrói a URL com base na URL base e no endpoint, e envia uma requisição HTTP GET.
        Permite adicionar parâmetros extras à requisição conforme a necessidade.

        :param endpoint: O caminho do endpoint a ser acessado (str).
        :param extra_params: Parâmetros adicionais para a requisição (dict, opcional).
        :return: Resposta da requisição em formato JSON (dict) ou um dicionário de erro (dict) em caso de falha.
        :raises requests.exceptions.RequestException: Se ocorrer um erro durante a requisição.
        """
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
            return {"error": str(e)}

    def get_filmes_populares_tmbd(self, time_window="day") -> dict:
        """
        Retorna os filmes mais populares do TMDB com base nas tendências diárias.

        :return: Um dicionário contendo os filmes populares.
        """
        time_window = "day"
        endpoint = f"/trending/movie/{time_window}" 
        return self.request(endpoint)

    def get_series_populares_tmbd(self, time_window="day") -> dict:
        """
        Retorna as séries mais populares do TMDB com base nas tendências diárias.

        :return: Um dicionário contendo os filmes populares.
        """
        endpoint = f"/trending/tv/{time_window}"
        return self.request(endpoint)