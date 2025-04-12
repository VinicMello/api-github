# Imports
import os
import requests
import pandas as pd
from datetime import datetime

# Environment Variables
TOKEN_GITHUB = os.getenv("GITHUB_TOKEN")
API_GITHUB_URL = os.getenv("API_GITHUB_URL")

# Class
class Dados:

    def __init__(self, owner):
        """
        """
        self.owner = owner
        self.token = TOKEN_GITHUB
        self.headers = {'Authorization': 'Bearer ' + self.token,
                        'X-GitHub-Api-Version': '2022-11-28'}
        self._overview_data = self._get_overview_data() 

    def _check_api_status(self, url):
        """
        """
        try:
            return requests.get(url=url, headers=self.headers).status_code == 200
        except requests.exceptions.RequestException as error:
            raise error
    
    def _get_overview_data(self):
        """
        """
        try:
            url = f'{API_GITHUB_URL}/users/{self.owner}'
            response = requests.get(url=url, headers=self.headers)
            return response.json()
        except requests.exceptions.RequestException as error:
            raise error

    @property
    def get_profile_url(self):
        """
        """
        return self._overview_data.get("html_url")

    @property
    def get_quantity_rep(self):
        """
        """
        return self._overview_data.get("public_repos")

    def collect_and_build_df_overview(self):
        """
        """
        overview_df = pd.DataFrame([self._overview_data]) 
        return overview_df

    def collect_repositories_and_build_df(self):
        """
        """
        # Obtém a URL base dos repositórios
        base_url_rep = self._overview_data.get("repos_url")

        # Verifica o status da API para a URL base
        self._check_api_status(url=base_url_rep)

        # Calcula a quantidade de páginas com base na quantidade de repositórios
        num_pages = round(int(self.get_quantity_rep)/30)

        # Lista para armazenar os dados que serão convertidos em DataFrame
        repos_data = []
        
        try:
            # Percorre as páginas de repositórios
            for page_num in range(1, num_pages + 1):
                    
                    # URL para cada página
                    url = f'{base_url_rep}?page={page_num}'

                    # Requisição e verifica o status da API
                    response = requests.get(url, headers=self.headers)
                    response.raise_for_status()

                    # Extrai as informações de cada repositório
                    for rep in response.json():
                        repos_data.append({
                        "created_at": rep.get("created_at"),
                        "name": rep.get("name"),
                        "full_name": rep.get("full_name"),
                        "description": rep.get("description"),
                        "language": rep.get("language"),
                        "html_url": rep.get("html_url"),
                        "updated_at": rep.get("updated_at"),
                    })

            # Cria o DataFrame com os dados coletados    
            df_repos = pd.DataFrame(repos_data)                
            return df_repos
        
        except Exception as error:
            raise error
    
    def add_column_processing_date(df):
        """
        """
        df['processing_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return df

# Main Cód.
my_rep = Dados("Netflix")

df = my_rep.collect_repositories_and_build_df()
overview_df = my_rep.collect_and_build_df_overview()



print()




