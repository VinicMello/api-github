import os
import time
import logging
import pandas as pd

DIR = os.getcwd()
DATA_PATH = os.path.join(DIR, 'src', 'data')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_all_data_from_folder(folder: str) -> pd.DataFrame:
    """
    Loads and concatenates all JSON files from a specific folder in the data directory.

    Args:
        folder (str): Folder name inside the 'data' directory.

    Returns:
        pd.DataFrame: A DataFrame containing the concatenated data.
    """
    dfs = []
    reference_path = os.path.join(DATA_PATH, folder)
    
    try:
        for file in os.listdir(reference_path):
            if file.endswith('.json'):
                df = pd.read_json(os.path.join(reference_path, file))
                dfs.append(df)

        return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
    
    except Exception as error:
        raise error

def save_df(df: pd.DataFrame, folder: str, filename: str) -> None:
    """
    Saves a DataFrame as a JSON file inside a specific folder in the data directory.

    Args:
        df (pd.DataFrame): DataFrame to be saved.
        folder (str): Folder name inside the 'data' directory.
        filename (str): Desired name of the saved file (without extension).
    """
    reference_path = os.path.join(DATA_PATH, folder)

    try:
        os.makedirs(reference_path, exist_ok=True)
        save_path = os.path.join(reference_path, f'{filename}.json')
        os.remove(save_path) if os.path.exists(save_path) else None
        df.to_json(save_path)

    except Exception as error:
        raise error

def main() -> None:
    """
    Main function to orchestrate the data transformation process.
    """
    start_time = time.time()

    try:
        logging.info("Saving consolidated dataframes...")
        df_overview = load_all_data_from_folder('overview')
        df_repositories = load_all_data_from_folder('repositories')

        save_df(df_overview, folder='final', filename='overview')
        save_df(df_repositories, folder='final', filename='repositories')

        del df_overview
        del df_repositories

    except Exception as error:
        raise error

    end_time = time.time()
    logging.info(f"Total processing time: {(end_time - start_time):.2f} seconds")

if __name__ == "__main__":
    main()