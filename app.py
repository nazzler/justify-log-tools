import requests
import json
import pandas as pd 
from config.client_config import CLIENT_SECRET, CLIENT_ID, API_ENDPOINT, TOKEN_URL, GRANT_TYPE
from config.spell_config import HEALING
from query.query_config import Codes, EventCasts
from query.query_utils import res_to_df


from query.query_utils import run_query

HEALING_EVENTS_DF = pd.DataFrame

params = {
    "client_secret": CLIENT_SECRET,
    "client_id": CLIENT_ID,
    "grant_type": GRANT_TYPE
}

response = requests.post(TOKEN_URL, data=params)
json_string = json.loads(response.text)
access_token = json_string["access_token"]

headers = {"Authorization": f"Bearer {access_token}"}

# TODO return these values as result of functions
EventCasts.reportCode = '"KG9va8WVgLnfYRAq"'
EventCasts.fightId = 1
EventCasts.startTime = 175475
EventCasts.endTime = 775751
EventCasts.dataType = "Casts"

casts = pd.DataFrame()
startEndDf = pd.DataFrame(
    [
        [EventCasts.startTime, "FIGHT START", EventCasts.reportCode],
        [EventCasts.endTime, "FIGHT END", EventCasts.reportCode]
    ],
    columns=['timestamp', 'type', 'reportId']
)

casts = casts.append(startEndDf)

for key in HEALING:
    EventCasts.abilityId = HEALING[key]
    events_query = EventCasts.event_cast_query_builder(
        EventCasts.reportCode, EventCasts.fightId, EventCasts.startTime, EventCasts.endTime, EventCasts.abilityId, EventCasts.dataType)
    res = run_query(query=events_query, head=headers, endpoint=API_ENDPOINT)
    json_data = res['data']['reportData']['report']['events']['data']
    if json_data:
        # res_to_df(json_data=json_data)
        data = pd.json_normalize(json_data)
        data['spellName'] = key
        data['reportId'] = EventCasts.reportCode.strip('"')
        casts = casts.append(data)
        casts = casts.sort_values(by='timestamp', ascending=True)
        casts = casts.drop(columns=['sourceMarker'])
        
casts.to_csv('.\\.data\\test.csv', index=False)

