import os
import requests
import pandas as pd
from typing import Dict, Any
from datetime import datetime

# Environment Variables
DIR = os.getcwd()
TOKEN_GITHUB = os.getenv("GITHUB_TOKEN")
API_GITHUB_URL = os.getenv("API_GITHUB_URL")

class Extract:
    """
    Class to interact with the GitHub API and extract user overview
    and repository data, saving results as structured JSON.
    """

    def __init__(self, owner: str) -> None:
        """
        Initialize the Extract class with a GitHub user/organization.

        Args:
            owner (str): GitHub username or organization.
        """
        self.owner = owner
        self.token = TOKEN_GITHUB
        self.headers = {
            'Authorization': 'Bearer ' + self.token,
            'X-GitHub-Api-Version': '2022-11-28'
        }
        self._overview_data = self._get_overview_data()
        self.base_data_path = os.path.join(DIR, 'src', 'data')

    def _check_api_status(self, url: str) -> bool:
        """
        Check if the GitHub API is responding properly.

        Args:
            url (str): API URL to test.

        Returns:
            bool: True if status code is 200, False otherwise.
        """
        try:
            return requests.get(url=url, headers=self.headers).status_code == 200
        
        except requests.exceptions.RequestException as error:
            raise error

    def _get_overview_data(self) -> Dict[str, Any]:
        """
        Get general profile data from the GitHub user.

        Returns:
            dict: JSON response with user overview data.
        """
        try:
            url = f'{API_GITHUB_URL}/users/{self.owner}'
            response = requests.get(url=url, headers=self.headers)
            return response.json()
        
        except requests.exceptions.RequestException as error:
            raise error

    @property
    def get_profile_url(self) -> str:
        """
        Return the user's GitHub profile URL.

        Returns:
            str: GitHub profile URL.
        """
        return self._overview_data.get("html_url")

    @property
    def get_quantity_rep(self) -> int:
        """
        Return the number of public repositories.

        Returns:
            int: Public repository count.
        """
        return self._overview_data.get("public_repos")

    def collect_and_build_df_overview(self) -> pd.DataFrame:
        """
        Create a DataFrame with the user's profile overview.

        Returns:
            pd.DataFrame: Overview data.
        """
        try:
            overview_df = pd.DataFrame([self._overview_data])
            overview_df = self.add_column_processing_date(overview_df)
            return overview_df
        
        except Exception as error:
            raise error

    def collect_repositories_and_build_df(self) -> pd.DataFrame:
        """
        Collect all repositories from the user and return as DataFrame.

        Returns:
            pd.DataFrame: Repository metadata.
        """
        base_url_rep = self._overview_data.get("repos_url")
        self._check_api_status(url=base_url_rep)
        num_pages = round(int(self.get_quantity_rep) / 30)
        repos_data = []

        try:
            for page_num in range(1, num_pages + 1):
                url = f'{base_url_rep}?page={page_num}'
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()

                for rep in response.json():
                    repos_data.append({
                        "created_at": rep.get("created_at"),
                        "id_owner": rep.get("owner", {}).get("id"),
                        "name": rep.get("name"),
                        "full_name": rep.get("full_name"),
                        "description": rep.get("description"),
                        "language": rep.get("language"),
                        "html_url": rep.get("html_url"),
                        "updated_at": rep.get("updated_at"),
                    })

            df_repos = pd.DataFrame(repos_data)
            df_repos = self.add_column_processing_date(df_repos)
            return df_repos

        except Exception as error:
            raise error

    @staticmethod
    def add_column_processing_date(df: pd.DataFrame) -> pd.DataFrame:
        """
        Add a column with the current processing date to the DataFrame.

        Args:
            df (pd.DataFrame): DataFrame to modify.

        Returns:
            pd.DataFrame: Updated DataFrame with processing_date column.
        """
        try:
            df['processing_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return df
        
        except Exception as error:
            raise error

    def save_df(self, df: pd.DataFrame, filename: str) -> None:
        """
        Save a DataFrame as a JSON file.

        Args:
            df (pd.DataFrame): DataFrame to save.
            filename (str): Folder name to save the file in.
        """
        try:
            os.makedirs(self.base_data_path, exist_ok=True)
            save_path = os.path.join(self.base_data_path, f'{filename}', f'{self.owner}.json')
            os.remove(save_path) if os.path.exists(save_path) else None
            df.to_json(save_path)

        except Exception as error:
            raise error