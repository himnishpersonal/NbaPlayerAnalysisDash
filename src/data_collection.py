from nba_api.stats.endpoints import playercareerstats, commonplayerinfo
from projections import player_projection
import pandas as pd


#Player INFO
player_id = '2544'
def get_player_metrics(player_id):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    player_info_data = player_info.get_data_frames()[0]
    #Career INFO
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_data = career_stats.get_data_frames()[0]
    career_data['PPG'] = career_data['PTS'] / career_data['GP']
    
    
    
    metrics_dict = {}
    metrics_dict['player_info'] = player_info_data
    #Year
    metrics_dict['Year'] = career_data['SEASON_ID'].apply(lambda x: f"{x[:4]}-{x[4:]}")
    #Career Points Per Game (PPG)
    metrics_dict['PPG'] = career_data['PTS'] / career_data['GP']
    #Field Goal Percentage (FG%)
    metrics_dict['FG%'] = (career_data['FGM'] / career_data['FGA']) * 100
    #Assist-to-Turnover Ratio (AST/TO)
    metrics_dict['AST/TO'] = career_data['AST'] / career_data['TOV']
    metrics_dict["TOV"] = career_data['TOV']
    #Usage Rate (USG%)
    metrics_dict['USG%'] = 100 * ((career_data['FGA'] + 0.44 * career_data['FTA'] + career_data['TOV']) * (career_data['MIN'] / 5)) / career_data['MIN']
    metrics_dict['REB'] = career_data['REB']
    
    #Advanced metrics: 
    # True Shooting Percentage (TS%)
    metrics_dict['TS%'] = (career_data['PTS'] / (2 * (career_data['FGA'] + 0.44 * career_data['FTA']))) * 100
    # Effective Field Goal Percentage (eFG%)
    metrics_dict['eFG%'] = ((career_data['FGM'] + 0.5 * career_data['FG3M']) / career_data['FGA']) * 100
    # Turnover Percentage (TOV%)
    metrics_dict['TOV%'] = (career_data['TOV'] / (career_data['FGA'] + 0.44 * career_data['FTA'] + career_data['TOV'])) * 100
    # Free Throw Rate (FTR)
    metrics_dict['FTR'] = (career_data['FTA'] / career_data['FGA']) * 100
    
    
    # #Projecton Model Data
    # projection_results = player_projection(metrics_dict)
    # metrics_dict['projections'] = projection_results
    
    
    return metrics_dict
    
metrics_dict = get_player_metrics(player_id)



