#given an encounter id and (optionally) a raid comp, get top 50 execution logs and their report code. TODO pagination
CODES = \
"""
  query get_report_code  {
      worldData{ 
        encounter (id: {encounter_id}){
          fightRankings(
            difficulty: {difficulty}
            metric: {metric}
            serverRegion: {region}
            filter: {filter}
          )
                  
        }        
      }
    
   }
"""

#given report code, get fight id, startTime, and endTime
FIGHT_INFO: """

    query get_fight_info {
    reportData {
        report (
        code: {reportCode}
        ) {
        fights (killType: Kills) {
            name
            difficulty
            id
            kill
            startTime
            endTime
        }

        }
        }
    }
"""
#given report code, get master mapping info such as pg and npc id-to-actualname, as well as abilities id-to-actualname
FIGHT_MASTER:"""
  query get_master {
    reportData {
        report (
        code: {reportCode} 
        ) {
        masterData {
            actors 
            {
            name
            gameID
            id
            }
           abilities {
            gameID
            name
            type
          }
        }
        }
    }
    }
    """


#given report code, fight id, startTime, and endTime, get all reports event TODO pagination
EVENTS = """
query get_events {
    reportData {
        report(
            code: {reportCode}
        ) {
            events(fightIDs: {fightId}, startTime: {startTime}, endTime: {endTime}, abilityID: {abilityId}, dataType: {dataType}) {
                data
            }
        }
    }
}
"""
