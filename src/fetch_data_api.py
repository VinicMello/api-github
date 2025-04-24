import time
import logging
import pandas as pd
from modules.extract import Extract

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

users_github = [
    "Netflix",
    "google",
    "microsoft",
    "facebook",      
    "apple",        
    "Amazon",        
    "airbnb",
    "spotify",
    "linkedin",
    "openai",        
    "databricks",
    "picpay",             
    "magalu",             
    "XPInc",              
    "nubank",             
    "quintoandar",        
    "globocom",           
    "C6Bank"
]

def main() -> None:
    """
    Collects data from several GitHub users and saves overview and repository info for each one.
    """
    start_time = time.time()
    
    for user in users_github:
        try:
            logging.info(f"Starting collection for user: {user}")
            user_github = Extract(owner=user)
            
            logging.info("Extracting...")
            df_overview = user_github.collect_and_build_df_overview()
            df_repositories = user_github.collect_repositories_and_build_df()

            logging.info("Saving...")
            user_github.save_df(df=df_overview, filename='overview')
            user_github.save_df(df=df_repositories, filename='repositories')

            logging.info(f"Process Finished...")
            time.sleep(1)

        except Exception as error:
            raise error
        
    end_time = time.time()
    logging.info(f"Total processing time: {(end_time - start_time):.2f} seconds")

if __name__ == "__main__":
    main()

    
