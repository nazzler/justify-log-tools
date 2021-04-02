import requests
import json
import pandas as pd
from config.client_config import CLIENT_SECRET, CLIENT_ID, API_ENDPOINT, TOKEN_URL, GRANT_TYPE, get_headers
from config.spell_config import HEALING
from query.query_config import EventCasts, CASTS_COLUMN_LIST
from query.query_utils import res_to_df, populate_empty_casts_df,  run_query, df_to_damage_table

headers = get_headers()

# TODO return these values as result of functions, only input needed is fight id and comp-filters
EventCasts.reportCode = '"KG9va8WVgLnfYRAq"'
EventCasts.fightId = 1
EventCasts.startTime = 175475
EventCasts.endTime = 775751
EventCasts.dataType = "Casts"

casts_df = populate_empty_casts_df(header_config=CASTS_COLUMN_LIST, start_time=EventCasts.startTime, end_time=EventCasts.endTime, report_code=EventCasts.reportCode)

for key in HEALING:
    EventCasts.abilityId = HEALING[key]
    events_query = EventCasts.event_cast_query_builder(EventCasts.reportCode, EventCasts.fightId, EventCasts.startTime, EventCasts.endTime, EventCasts.abilityId, EventCasts.dataType)
    res = run_query(query=events_query, head=headers, endpoint=API_ENDPOINT)
    json_data = res['data']['reportData']['report']['events']['data']
    if json_data:
        casts_df = res_to_df(data=json_data, spell=key, report_code=EventCasts.reportCode, baseline_df=casts_df, accepted_columns=CASTS_COLUMN_LIST)

damage_events = df_to_damage_table(df=casts_df)


print(casts_df)
print(damage_events)

# casts.to_csv('.\\.data\\test.csv', index=False)
