import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('football_data.csv')

# Sidebar for user input
st.sidebar.title("Football Dashboard")
selected_team = st.sidebar.selectbox('Select Team', df['Team'].unique())
selected_player = st.sidebar.selectbox('Select Player', df[df['Team'] == selected_team]['Player'].unique())

# Display selected player statistics
player_stats = df[df['Player'] == selected_player].iloc[0]
st.write(f"## {selected_player} - {selected_team}")
st.write(f"Matches: {player_stats['Matches']}")
st.write(f"Goals: {player_stats['Goals']}")
st.write(f"Assists: {player_stats['Assists']}")
st.write(f"Minutes Played: {player_stats['Minutes Played']}")
st.write(f"Pass Accuracy: {player_stats['Pass Accuracy']}%")
st.write(f"Tackles: {player_stats['Tackles']}")

# Bar chart for player statistics
st.write("### Player Performance")
fig = px.bar(
    x=['Goals', 'Assists', 'Minutes Played', 'Pass Accuracy', 'Tackles'],
    y=[player_stats['Goals'], player_stats['Assists'], player_stats['Minutes Played'], player_stats['Pass Accuracy'], player_stats['Tackles']],
    labels={'x': 'Metric', 'y': 'Value'},
    title='Player Performance'
)
st.plotly_chart(fig)

# Aggregate statistics for the selected team
team_stats = df[df['Team'] == selected_team].sum()
st.write(f"## {selected_team} - Team Statistics")
st.write(f"Total Matches: {team_stats['Matches']}")
st.write(f"Total Goals: {team_stats['Goals']}")
st.write(f"Total Assists: {team_stats['Assists']}")
st.write(f"Total Minutes Played: {team_stats['Minutes Played']}")
st.write(f"Average Pass Accuracy: {team_stats['Pass Accuracy'] / len(df[df['Team'] == selected_team])}%")
st.write(f"Total Tackles: {team_stats['Tackles']}")

# Pie chart for team contribution
st.write("### Team Contribution")
team_contrib = df[df['Team'] == selected_team].groupby('Player').sum()
fig = px.pie(
    team_contrib,
    values='Goals',
    names=team_contrib.index,
    title='Goals Contribution by Player'
)
st.plotly_chart(fig)
