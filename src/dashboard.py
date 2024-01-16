import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from data_collection import get_player_metrics
import plotly.express as px
import pandas as pd
from nba_api.stats.endpoints import commonplayerinfo
from dash import callback_context
from dash.exceptions import PreventUpdate


app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
player_id = '2544'  
metrics_dict = get_player_metrics(player_id)
player_info = metrics_dict['player_info']

prelim_info = {
    'First Name': player_info['FIRST_NAME'],
    'Last Name' : player_info['LAST_NAME'],
    'Country' : player_info['COUNTRY'],
    'Height' : player_info['HEIGHT'],
    'Position': player_info['POSITION'],
    'TEAM_NAME': player_info["TEAM_NAME"]
}

df_line = pd.DataFrame({
    "PPG" : metrics_dict['PPG'],
    "Years" : metrics_dict['Year']
})

df_line_fg = pd.DataFrame({
    "FG" : metrics_dict['FG%'],
    "Years" : metrics_dict['Year']
})

df_scatter = pd.DataFrame({
    "AST/TO" : metrics_dict['AST/TO'],
    "TOV" : metrics_dict['TOV'],
    "Years" : metrics_dict['Year']
})

df_area = pd.DataFrame({
    "USG%" : metrics_dict['USG%'],
    "Years" : metrics_dict['Year']
})

area_fig = px.area(df_area, x="Years", y="USG%", title="Usage Rate Over Time")
line_fig = px.line(df_line, x="Years", y="PPG",title="PPG Progression")
bar_fig = px.line(df_line_fg,x="Years", y="FG",title="FG% Progression")
scatter_fig = px.scatter(df_scatter, x="Years", y="AST/TO", size="TOV", title="Assist-to-Turnover Ratio (AST/TO)")


app.layout = html.Div(children=[
    # Preliminary Information Section
    html.Div(style={
            'background-color': '#1a1a1a',
            'color': 'orange',
            'border': '1px solid #333',
            'padding': '10px',
            'border-radius': '10px',
            'margin-right': '500px',
        },
                     children=[
                         html.H1(children='NBA Player Analysis Dashboard', style={'text-align': 'left'})
                     ]),
    html.Div(
    style={
            'position': 'absolute',
            'top': '10px',
            'right': '10px',
            'border': '1px solid #ccc',
            'padding': '10px',
            'border-radius': '10px',
            'width': '450px',
            'height': '78px',
            'background-color': '#333',
        },
    children=[
            dcc.Input(
                id='player-search-input',
                type='text',
                placeholder='Enter player name',
                debounce=True,
                style={'border-radius': '5px', 'padding': '8px', 'margin-right': '8px'}
            ),
            html.Button('Search', id='search-button', n_clicks=0,
                        style={'border-radius': '5px', 'padding': '8px', 'background-color': '#555', 'color': '#fff'})
        ]
    ),
    html.Div(
        id='player-info',
        style={
            'position': 'absolute',
            'top': '10px',
            'right': '10px',
            'border': '1px solid #ccc',
            'padding': '20px',
            'border-radius': '10px',
            'width': '400px',
            'text-align': 'center',
            'margin-top': '140px',
            'background-color': '#333',
            'color': 'orange',
        },
        children=[
            html.H2('Player Information'),
            html.Table(id='player-info-table',  # Assigning an id here
                children=[
                    html.Tr([html.Th(key), html.Td(value)]) for key, value in prelim_info.items()
                ]
            )
        ]
    ),
    html.Div(
        id='advanced-metrics',
        style={
            'border': '1px solid #ccc',
            'padding': '20px',
            'border-radius': '10px',
            'margin-top': '320px',
            'position': 'absolute',
            'right': '10px',
            'width': '400px',
            'text-align': 'center',
            'height': '221px',
            'background-color': '#333',
            'color': 'orange',
        },
        children=[
            html.H2('Advanced Metrics'),
            html.Table(id='advanced-metrics-table',  # Assigning an id here
                children=[
                    html.Tr([html.Th('True Shooting Percentage (TS%)'), html.Td(f"{metrics_dict['TS%'].iloc[-1]:.2f}")]),
                    html.Tr([html.Th('Effective Field Goal Percentage (eFG%)'), html.Td(f"{metrics_dict['eFG%'].iloc[-1]:.2f}")]),
                    html.Tr([html.Th('Turnover Percentage (TOV%)'), html.Td(f"{metrics_dict['TOV%'].iloc[-1]:.2f}")]),
                    html.Tr([html.Th('Free Throw Rate (FTR)'), html.Td(f"{metrics_dict['FTR'].iloc[-1]:.2f}")]),
                ]
            )
        ]
    ),
    html.Div(
        id='graph',
        style={
            'border': '1px solid #ccc',
            'padding': '5px',
            'border-radius': '10px',
            'margin-top': '40px',
            'margin-right': '500px',
            'background-color': '#333',
            'color': 'orange',
        },
        children=[
            dcc.RadioItems(
                id='graph-selector',
                options=[
                    {'label': 'PPG Progression', 'value': 'ppg-graph'},
                    {'label': 'FG% Comparison', 'value': 'fg-graph'},
                    {'label': 'AST/TO Scatter Plot', 'value': 'ast-to-scatter-plot'},
                    {'label': 'Usage Rate Over Time', 'value': 'usage-rate-area-chart'}
                ],
                value='ppg-graph',  
                labelStyle={'display': 'block'}  
            ),

            dcc.Graph(id='graph-container', style={'width': '95%', 'display': 'inline-block'})
        ]
    )
], style={'font-family': 'Your Desired Font, sans-serif','background-color': 'orange'})

    
def get_player_id_by_name(player_name):
    player_info = commonplayerinfo.CommonPlayerInfo(player_name).get_data_frames()[0]
    if not player_info.empty:
        player_id = player_info['PERSON_ID'].iloc[0]
        return player_id
    else:
        return None
    
@app.callback(
    Output('graph-container', 'figure'),
    [Input('graph-selector', 'value')]
)
def update_graph(selected_graph):
    if selected_graph == 'ppg-graph':
        return line_fig
    elif selected_graph == 'fg-graph':
        return bar_fig
    elif selected_graph == 'ast-to-scatter-plot':
        return scatter_fig
    elif selected_graph == 'usage-rate-area-chart':
        return area_fig



# def update_graph(selected_graph):
#     if player_id is not None:
#         metrics_dict = get_player_metrics(player_id)
        
#         if selected_graph == 'ppg-graph':
#             df_line = pd.DataFrame({
#                 "PPG": metrics_dict['PPG'],
#                 "Years": metrics_dict['Year']
#             })
#             fig = px.line(df_line, x="Years", y="PPG", title="PPG Progression")
#         elif selected_graph == 'fg-graph':
#             df_line_fg = pd.DataFrame({
#                 "FG": metrics_dict['FG%'],
#                 "Years": metrics_dict['Year']
#             })
#             fig = px.line(df_line_fg, x="Years", y="FG", title="FG% Progression")
#         elif selected_graph == 'ast-to-scatter-plot':
#             df_scatter = pd.DataFrame({
#                 "AST/TO": metrics_dict['AST/TO'],
#                 "TOV": metrics_dict['TOV'],
#                 "Years": metrics_dict['Year']
#             })
#             fig = px.scatter(df_scatter, x="Years", y="AST/TO", size="TOV", title="Assist-to-Turnover Ratio (AST/TO)")
#         elif selected_graph == 'usage-rate-area-chart':
#             df_area = pd.DataFrame({
#                 "USG%": metrics_dict['USG%'],
#                 "Years": metrics_dict['Year']
#             })
#             fig = px.area(df_area, x="Years", y="USG%", title="Usage Rate Over Time")
#         else:
#             fig = None

#         return fig

#     raise PreventUpdate

# @app.callback(
#     [
#         Output('player-info-table', 'children'),
#         Output('advanced-metrics-table', 'children')
#     ],
#     [Input('search-button', 'n_clicks')],
#     [State('player-search-input', 'value')]
# )

# def update_dashboard(n_clicks, player_name):
#     if n_clicks is None or player_name is None:
#         raise PreventUpdate
#     player_id = get_player_id_by_name(player_name)
#     if player_id is not None:
#         metrics_dict = get_player_metrics(player_id)
#         prelim_info = {
#             'First Name': metrics_dict['player_info']['FIRST_NAME'],
#             'Last Name': metrics_dict['player_info']['LAST_NAME'],
#             'Country': metrics_dict['player_info']['COUNTRY'],
#             'Height': metrics_dict['player_info']['HEIGHT'],
#             'Position': metrics_dict['player_info']['POSITION'],
#             'TEAM_NAME': metrics_dict['player_info']["TEAM_NAME"]
#         }
#         return (
#             [html.Tr([html.Th(key), html.Td(value)]) for key, value in prelim_info.items()],
#             [
#                 html.Tr([html.Th('True Shooting Percentage (TS%)'), html.Td(f"{metrics_dict['TS%'].iloc[-1]:.2f}")]),
#                 html.Tr([html.Th('Effective Field Goal Percentage (eFG%)'),
#                          html.Td(f"{metrics_dict['eFG%'].iloc[-1]:.2f}")]),
#                 html.Tr([html.Th('Turnover Percentage (TOV%)'), html.Td(f"{metrics_dict['TOV%'].iloc[-1]:.2f}")]),
#                 html.Tr([html.Th('Free Throw Rate (FTR)'), html.Td(f"{metrics_dict['FTR'].iloc[-1]:.2f}")]),
#             ]
#         )
#     else:
#         return [html.Tr([html.Th('Player not found'), html.Td('')])] * 2 + [None]
            
            
        







# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
