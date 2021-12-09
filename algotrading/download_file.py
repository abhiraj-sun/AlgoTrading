import pandas as pd
from datetime import datetime
import requests
import numpy as np

url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)
token_df["expiry"] = pd.to_datetime(token_df['expiry'])
token_df = token_df.astype({'strike': float})
token_df.to_csv(r'/Volumes/Data/AppDevelopment/python/SmartAPIdata.csv', header=True, index=False)