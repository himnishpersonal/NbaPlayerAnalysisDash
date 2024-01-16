NBA Player Analysis Dashboard

Overview
The NBA Player Analysis Dashboard is a web application built using Dash and Plotly, offering detailed insights into a basketball player's performance metrics over time. Users can explore various aspects of a player's career, including points per game (PPG) progression, field goal percentage (FG%), assist-to-turnover ratio (AST/TO), and usage rate (USG%).

Features
Player Search: Enter the name of an NBA player to instantly retrieve their comprehensive statistical information.
Dynamic Graphs: Interactive graphs display key metrics, allowing users to visualize and analyze a player's performance trends.
Advanced Metrics: Access advanced metrics such as true shooting percentage (TS%), effective field goal percentage (eFG%), turnover percentage (TOV%), and free throw rate (FTR).
Usage
Run the application using python app.py.
Open a web browser and navigate to http://localhost:8050/.
Enter the name of the desired NBA player in the search bar.
Explore the player's detailed information, including career statistics and advanced metrics.
Use the dynamic graphs to gain insights into the player's progression in various aspects of the game.
Project Structure
app.py: Main application file containing the Dash app layout and callbacks.
data_collection.py: Module for collecting player metrics from the NBA API.
projections.py: Module for player projection modeling.
requirements.txt: List of Python dependencies.
