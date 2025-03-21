import pandas as pd
import os

class ManipulaDiretorio:
    def __init__(self, path_download, data_json):
        self.path_download = path_download
        self.data_json = data_json
    
    def create_directory(self):
        if not os.path.exists(self.path_download):
            os.makedirs(self.path_download)
            print("Diretório criado...")
        else:
            print("Diretório já existe...pulando")

    def json_to_csv(self):
        results_data = self.data_json.get("results")
        df = pd.DataFrame(results_data)
        saida_csv = df.to_csv('downloads/teste.csv', encoding='utf-8', index=False)

