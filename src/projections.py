from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime


def calculate_age(birthdate):
    birthdate = birthdate.squeeze()
    birthdate = datetime.strptime(birthdate, '%Y-%m-%dT%H:%M:%S')
    today = datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def train_linear_regression(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model


def player_projection(metrics_dict):
    player_info = metrics_dict['player_info']
    
    # Calculate age
    birthdate = player_info['BIRTHDATE']
    age = calculate_age(birthdate)
    
    # Features and targets
    features = ['PPG', 'APG', 'REB', 'AGE', 'MIN']
    target_ppg = 'NextYear_PPG'
    target_apg = 'NextYear_APG'
    target_reb = 'NextYear_REB'
    
    X = [[
        metrics_dict['PPG'],
        metrics_dict['AST/TO'],
        metrics_dict['REB'],
        age
    ]]
    
    # Targets
    y_ppg = [metrics_dict[target_ppg]]
    y_apg = [metrics_dict[target_apg]]
    y_reb = [metrics_dict[target_reb]]
    
    # Train linear regression models
    model_ppg = train_linear_regression(X, y_ppg)
    model_apg = train_linear_regression(X, y_apg)
    model_reb = train_linear_regression(X, y_reb)

    # Make predictions
    ppg_predictions = model_ppg.predict(X)[0]
    apg_predictions = model_apg.predict(X)[0]
    reb_predictions = model_reb.predict(X)[0]
    
    # Create a dictionary with the projections
    projections = {
        'Projected_PPG': ppg_predictions,
        'Projected_APG': apg_predictions,
        'Projected_REB': reb_predictions,
        'Age': age
    }
    
    return projections
