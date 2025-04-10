import os
import json
import requests

TOKEN = os.getenv("GITHUB_TOKEN")
URL = 'https://api.github.com'

class Dados:

    def __init__(self, owner):
        """
        """
        self.owner = owner
        self.token = TOKEN
        self.headers = {'Authorization': 'Bearer ' + self.token,
                        'X-GitHub-Api-Version': '2022-11-28'}
        self._overview_data = self._get_overview_data() 
        self.url_profile = self.profile_url
        self.overview = self.format_overview_profile
    
    def check_api_status(self):
        """
        """
        try:
            return requests.get(url=URL, headers=self.headers).status_code == 200
        except requests.exceptions.RequestException as error:
            raise error
    
    def _get_overview_data(self):
        """
        """
        try:
            url = f'{URL}/users/{self.owner}'
            response = requests.get(url=url, headers=self.headers)
            return response.json()
        except requests.exceptions.RequestException as error:
            raise error
    
    @property
    def format_overview_profile(self):
        """
        """
        return json.dumps(self._get_overview_data(), indent=4)
    
    @property
    def profile_url(self):
        """
        """
        return self._overview_data.get("html_url")

    def get_repos(self):
        """
        """
        url_rep = self._overview_data.get("repos_url")
        print()

    
my_rep = Dados("Netflix")
print(my_rep.overview)
# print(my_rep.token)
# print(my_rep.check_api_status())
# rep = my_rep.overview_rep()

# url_rep = rep['repos_url']
# response = requests.get(url=url_rep, headers=my_rep.headers)

# teste = response.json()
# for rep in teste:
#     print(rep['name'])
print()




