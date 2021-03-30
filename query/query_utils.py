import json
import requests
import pandas as pd 

def run_query(query: str, head: str, endpoint: str) -> dict:
  request = requests.post(endpoint, json={'query': query}, headers=head)
  if request.status_code == 200:
    return request.json()
  else:
    raise Exception(f"Query failed to run with a {request.status_code}.")

def res_to_df(data: dict):
  """
  Transform api results to pandas DataFrame  
  """
  temp = pd.json_normalize(data)
  return temp
