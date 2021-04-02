import json
import requests
import pandas as pd
from typing import List

def run_query(query: str, head: str, endpoint: str) -> dict:
  request = requests.post(endpoint, json={'query': query}, headers=head)
  if request.status_code == 200:
    return request.json()
  else:
    raise Exception(f"Query failed to run with a {request.status_code}.")


def populate_empty_casts_df(header_config:dict, start_time: int, end_time: int, report_code:str) -> pd.DataFrame():
  """
  Add START and END row to cast df
  """
  df = pd.DataFrame(header_config, index=[])
  add_df = pd.DataFrame(
        [
            [start_time, "FIGHT START", -1, "encounter_start", report_code],
            [end_time, "FIGHT END", -1, "encounter_end", report_code]
        ],
        columns=['timestamp', 'type', 'abilityGameID', 'spellName', 'reportId']
    )
  df = df.append(add_df)
  return df

def res_to_df(data: dict, spell:str, report_code: str, baseline_df: pd.DataFrame(), accepted_columns=List[str]) -> pd.DataFrame():
  """
  Transform healing casts api results to pandas DataFrame and do stuff in between 
  """
  data_df = pd.json_normalize(data)
  data_df['spellName'] = spell
  data_df['reportId'] = report_code
  baseline_df = baseline_df.append(data_df)
  baseline_df = baseline_df.sort_values(by='timestamp', ascending=True)
  baseline_df['reportId'] = report_code.strip('"')
  baseline_df = baseline_df[accepted_columns]
  baseline_df = baseline_df.reset_index(drop=True)
  return baseline_df


def df_to_damage_table(df: pd.DataFrame()) -> pd.DataFrame: 
  df['seconds_after_previous_event'] = (df['timestamp'] - df['timestamp'].shift(1))/1000
  df['seconds_after_start'] = (df['timestamp'] - df.loc[df['type'] == "FIGHT START", 'timestamp'].values[0])/1000

  i = 0
  df['event_group'] = ""
  for idx, value in df['seconds_after_previous_event'].iteritems():
      if idx == 0:
          df.at[idx, 'event_group'] = "START"
      elif idx == df.index[-1]:
          df.at[idx, 'event_group'] = "END"
      else:
          if value > 3.5:
              i = i + 1
              event_group = "DAMAGE EVENT " + str(i)
              df.at[idx, 'event_group'] = event_group
          elif idx != 0:
              df.at[idx, 'event_group'] = event_group

  max = df.groupby(['event_group'], sort=False)['timestamp'].max()
  min = df.groupby(['event_group'], sort=False)['timestamp'].min()
  df = df.join(min, on=['event_group'], how='left', rsuffix='_min')
  df = df.join(max, on=['event_group'], how='left', rsuffix='_max')
  df['timestamp_min'] = df['timestamp_min'] - 3000
  df['timestamp_max'] = df['timestamp_max'] + 3000

  damage_table = df.groupby(['event_group'], sort=False).agg({'timestamp_min': 'min', 'timestamp_max': 'max'})

  return damage_table 

