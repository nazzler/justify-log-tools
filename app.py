import requests
import json
from config.client_config import *
from config.spell_config import *
from query.query_config import *

from query.query_utils import run_query

params = {
    "client_secret": CLIENT_SECRET,
    "client_id": CLIENT_ID,
    "grant_type": GRANT_TYPE
}

response = requests.post(TOKEN_URL, data=params)
json_string = json.loads(response.text)
access_token = json_string["access_token"]

headers = {"Authorization": f"Bearer {access_token}"}
res = run_query(query=TOP50X, head=headers, endpoint=API_ENDPOINT)

print(res)

