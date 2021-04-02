import requests
import json
import pandas as pd

CLIENT_ID = ""
CLIENT_SECRET = ""
TOKEN_URL = "https://www.warcraftlogs.com/oauth/token"
API_ENDPOINT = "https://www.warcraftlogs.com/api/v2/client"
GRANT_TYPE = "client_credentials"


def get_headers():
    params = {
        "client_secret": CLIENT_SECRET,
        "client_id": CLIENT_ID,
        "grant_type": GRANT_TYPE
    }


    response = requests.post(TOKEN_URL, data=params)
    json_string = json.loads(response.text)
    access_token = json_string["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    
    return headers
