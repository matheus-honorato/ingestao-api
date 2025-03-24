import pandas as pd
import os
import datetime

class ManipulaDiretorio:
    def __init__(self, path_download, data_json):
        self.path_download = path_download
        self.data_json = data_json
        self.name_file = None
    
    def create_directory(self):
        if not os.path.exists(self.path_download):
            os.makedirs(self.path_download)
            print("Diretório criado...")
        else:
            print("Diretório já existe...pulando")

    def generate_file_name(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        self.name_file = f"data_{timestamp}.csv"

    def json_to_csv(self):
        path_file = os.path.join(self.path_download, self.name_file)
        results_data = self.data_json.get("results")
        df = pd.DataFrame(results_data)
        df.to_csv(path_file, encoding='utf-8', index=False)

