import requests
import json
from config.config import CLIENT_ID, CLIENT_SECRET, TOKEN_URL, API_ENDPOINT, GRANT_TYPE
from query.query_utils import run_query
from query.query_config import JUSTIFY

params = {
    "client_secret": CLIENT_SECRET,
    "client_id": CLIENT_ID,
    "grant_type": GRANT_TYPE
}

response = requests.post(TOKEN_URL, data=params)
json_string = json.loads(response.text)
access_token = json_string["access_token"]

headers = {"Authorization": f"Bearer {access_token}"}
# result = run_query(query=JUSTIFY, head=headers, endpoint=API_ENDPOINT)