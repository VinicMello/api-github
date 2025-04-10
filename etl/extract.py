import os
import json
import requests

TOKEN = os.getenv("GITHUB_TOKEN")

class Dados:

    def __init__(self, owner):
        """
        """
        self.owner = owner
        self.url = 'https://api.github.com'
        self.token = TOKEN
        self.headers = {'Authorization': 'Bearer ' + self.token,
                        'X-GitHub-Api-Version': '2022-11-28'}
    
    def check_api_status(self):
        """
        """
        try:
            return requests.get(url=self.url, headers=self.headers).status_code == 200
        except requests.exceptions.RequestException as error:
            raise error
    
    def overview_rep(self):
        """
        """
        try:
            url = f'{self.url}/users/{self.owner}'
            response = requests.get(url=url, headers=self.headers)
            return json.dumps(response.json(), indent=4)
        except requests.exceptions.RequestException as error:
            raise error

    
my_rep = Dados("VinicMello")
print(my_rep.token)
print(my_rep.check_api_status())
print(my_rep.overview_rep())




