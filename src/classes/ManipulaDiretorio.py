import pandas as pd
import os

class ManipulaDiretorio:
    def __init__(self, path_download):
        self.path_download = path_download
    
    def criar_diretorio(self):
        if not os.path.exists(self.path_download):
            os.makedirs(self.path_download)
            print("Diretório criado...")
        else:
            print("Diretório já existe...pulando")
