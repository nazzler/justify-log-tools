import json
import requests
import pandas as pd 

def run_query(query: str, head: str, endpoint: str):
  request = requests.post(endpoint, json={'query': query}, headers=head)
  if request.status_code == 200:
    return request.json()
  else:
    raise Exception(f"Query failed to run with a {request.status_code}.")

def query_builder(args: str):
  """
 Based on user input, construct first query to get reports code. 
  """
  return query 

def res_to_df(res: str):
  """
  Transform api call results to pandas DataFrame
  """

  

  return df

