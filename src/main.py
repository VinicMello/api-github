import os
import pandas as pd
from modules.extract import Dados

# Lista de empresas
owners = ["Netflix"]

# Lista para armazenar os DataFrames
dfs = []

# Itera sobre as empresas e coleta os dados
for owner in owners:
    my_rep = Dados(owner=owner)
    df = my_rep.collect_repositories_and_build_df()
    dfs.append(df)

# Concatena os DataFrames em um único
consolidated_df = pd.concat(dfs, ignore_index=True)

consolidated_df.head()

print()

