import pandas as pd 

CASTS_COLUMN_LIST = {'timestamp':int(), 
                     'type':str(),
                     'abilityGameID':int(), 
                     'spellName':str(), 
                     'reportId':str()}



class Codes:

    def __init__(self, codeEncounterId, codeDifficulty, codeMetric, codeRegion, codeFilter):
            self.codeEncounterId = codeEncounterId
            self.codeDifficulty = codeDifficulty
            self.codeMetric = codeMetric
            self.codeRegion = codeRegion
            self.codeFilter = codeFilter
      
    def code_query_builder(codeEncounterId, codeDifficulty, codeMetric, codeRegion, codeFilter):
      
      CODES = f"""
      query get_report_code  {{
        worldData{{
          encounter (id: {codeEncounterId}){{
            fightRankings(
              difficulty: {codeDifficulty}
              metric: {codeMetric}
              serverRegion: {codeRegion}
              filter: {codeFilter}
                )
            }}
          }}
      }}
      """
      return CODES

class FightInfo: 
#Given a reportCode, returns fightId, startTime, endTime
  
  def __init__(self, reportCode):
    self.reportCode = reportCode

  def fight_info_query_builder(reportCode):

    FIGHT_INFO: f"""

    query get_fight_info {{
    reportData {{
        report (
        code: {reportCode}
        ) {{
        fights (killType: Kills) {{
            name
            difficulty
            id
            kill
            startTime
            endTime
        }}

        }}
        }}
    }}
    """
    return FIGHT_INFO
    
# #given report code, get master mapping info such as pg and npc id-to-actualname, as well as abilities id-to-actualname
# FIGHT_MASTER:f"""
#   query get_master {{
#     reportData {{
#         report (
#         code: {reportCode}
#         ) {{
#         masterData {{
#             actors
#             {{
#             name
#             gameID
#             type
#             subType
#             }}
#           abilities {{
#             gameID
#             name
#             type
#           }}
#         }}
#         }}
#     }}
#     }}
#     """
class EventCasts:

  def __init__(self, reportCode, fightId, startTime, endTime, abilityId, dataType):
      self.reportCode = reportCode
      self.fightId = fightId
      self.startTime = startTime
      self.endTime = endTime
      self.abilityId = abilityId
      self.dataType = dataType

  def event_cast_query_builder(reportCode, fightId, startTime, endTime, abilityId, dataType):
    EVENT_CASTS = f"""
      query get_events
      {{
          reportData
          {{
              report(code: {reportCode})
              {{
                  events(fightIDs: {fightId}, startTime: {startTime}, endTime: {endTime}, abilityID: {abilityId}, dataType: {dataType})
                  {{
                      data
                  }}
              }}
          }}
      }}
      """
    return EVENT_CASTS
