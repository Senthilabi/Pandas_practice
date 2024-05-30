import pandas as pd 
import numpy as np 
import plotly.express as px
import matplotlib.pyplot as plt 
import streamlit as st 
import plotly.graph_objects as go
# Streamlit app layout
st.set_page_config(page_title='Player DashBoard',page_icon=':soccer:',
                     layout="wide")

st.title('Dashboard of players:soccer:')
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
st.sidebar.title('Player selection')
# Load data from Excel file
excel_file = 'Player Data1.xlsx'
xl=pd.ExcelFile(excel_file)
xlsheets=xl.sheet_names
#xlsheets
# Read each sheet into a separate DataFrame
text_area_data = pd.read_excel(excel_file, sheet_name=xlsheets[0])
circle_score_data = pd.read_excel(excel_file, sheet_name=xlsheets[1])
radar_chart1_data = pd.read_excel(excel_file, sheet_name=xlsheets[2])
radar_chart2_data = pd.read_excel(excel_file, sheet_name=xlsheets[3])
radar_chart3_data = pd.read_excel(excel_file, sheet_name=xlsheets[5])
radar_chart4_data = pd.read_excel(excel_file, sheet_name=xlsheets[6])
Mid_text_area_data = pd.read_excel(excel_file, sheet_name=xlsheets[4])
circle_score_data['TSP Score']=circle_score_data['TSP Score']*100
df=circle_score_data.merge(radar_chart1_data, how ='outer',on='Player')
df=df.merge(radar_chart2_data, how ='outer',on='Player')
df=df.merge(radar_chart3_data,how='outer',on='Player')
df=df.merge(radar_chart4_data,how='outer',on='Player')
df=df.round(2)
player_list=df['Player'].to_list()

#player_list
selected_player=st.sidebar.selectbox('Select', player_list,key='1')
sp_details=df[(df['Player']==selected_player)|
                (df['Player']=='Ideal Left Winger' )]
#ip_details=df[df['Player']=='Ideal Left Winger']
sp_details.drop('TSP Score',axis=1,inplace=True)
#ip_details
def radar_chart1(df2):

    categories=list(df2.columns[1:])

    fig = go.Figure()


    for i in range(df2.shape[0]):
        fig.add_trace(go.Scatterpolar(
          r=list(df2.iloc[i,1:]),
          theta=categories,
          fill='toself',
          name=df2.iloc[i,0]
    ))
    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 100]
        )),
      showlegend=False
    )

    return  fig

#sp_details
v=sp_details.iloc[0,1]

circle_score = v
fig_circle = go.Figure(go.Indicator(
mode="gauge+number",
value=circle_score,
title={'text': "Score"},
gauge={
    'axis': {'range': [None, 100]},
    'bar': {'color': "darkblue"},
    'steps': [
        {'range': [0, 50], 'color': "lightgray"},
        {'range': [50, 75], 'color': "gray"},
        {'range': [75, 100], 'color': "darkgray"}
    ],
    'threshold': {
        'line': {'color': "red", 'width': 4},
        'thickness': 0.75,
        'value': 90}
    }
))
st.sidebar.plotly_chart(fig_circle,height=500)
st.sidebar.subheader(selected_player)
df1=Mid_text_area_data
df1=df1[df1['Player']==selected_player]
m1=list(df1.columns)[1]
v1=df1.iloc[0,1]
m2=list(df1.columns)[2]
v2=df1.iloc[0,2]
m3=list(df1.columns)[3]
v3=df1.iloc[0,3]
m4=list(df1.columns)[4]

df1[m4]=df1[m4].dt.strftime('%d-%m-%Y')
v4=df1.iloc[0,4]
st.sidebar.metric(m1,v1)
st.sidebar.metric(m2,v2)
st.sidebar.metric(m3,v3)
st.sidebar.metric(m4,v4)


#Text Row
c11,c12=st.columns((2))
t_c11=list(text_area_data.columns)[0]
t_v11=text_area_data.iloc[0,0]
c11.metric(t_c11,t_v11)
t_c12=list(text_area_data.columns)[1]
t_v12=text_area_data.iloc[0,1]
c12.metric(t_c12,t_v12)

c1,c2,c3,c4,c5,c6 = st.columns([3,3,3,3,3,3])


t_c3=list(text_area_data.columns)[2]
t_v31=text_area_data.iloc[0,2]
t_v32=text_area_data.iloc[1,2]
t_v33=text_area_data.iloc[2,2]
t_v34=text_area_data.iloc[3,2]
t_v35=text_area_data.iloc[4,2]
t_v36=text_area_data.iloc[5,2]
c1.metric(t_c3,t_v31)
#c2.metric('',t_v31)
c2.metric('',t_v32)
c3.metric('',t_v33)
c4.metric('',t_v34)
c5.metric('',t_v35)
c6.metric('',t_v36)

#t_v32,t_v33,t_v34,t_v35
c1,c2,c3,c4,c5,c6 = st.columns([3,3,3,3,3,3])


t_c3=list(text_area_data.columns)[3]
t_v31=text_area_data.iloc[0,3]
t_v32=text_area_data.iloc[1,3]
t_v33=text_area_data.iloc[2,3]
t_v34=text_area_data.iloc[3,3]
t_v35=text_area_data.iloc[4,3]
t_v36=text_area_data.iloc[5,3]
c1.metric(t_c3,t_v31)
#c2.metric('',t_v31)
c2.metric('',t_v32)
c3.metric('',t_v33)
c4.metric('',t_v34)
c5.metric('',t_v35)
c6.metric('',t_v36)

c11,c12=st.columns((2))
t_c11=list(text_area_data.columns)[4]
t_v11=text_area_data.iloc[0,4]
c11.metric(t_c11,t_v11)
t_c12=list(text_area_data.columns)[5]
t_v12=text_area_data.iloc[0,5]
c12.metric(t_c12,t_v12)





# Second Row
col3, col4 = st.columns(2)
df1=sp_details.iloc[:,1:8]
with col3:
    st.subheader('Chart-1')
    radar_fig1 = radar_chart1(df1)
    st.plotly_chart(radar_fig1)
    
with col4:
    st.subheader('Chart-2')
    df=sp_details.iloc[:,8:18]
    radar_fig1 = radar_chart1(df)
    st.plotly_chart(radar_fig1)
    
# Third Row
col5, col6= st.columns(2)

with col5:
    st.subheader('Chart-3')
    df=sp_details.iloc[:,18:25]
    radar_fig1 = radar_chart1(df)
    st.plotly_chart(radar_fig1)
    
with col6:
    st.subheader('Chart-4')
    df1=sp_details.iloc[:,25:]
    l=list(sp_details.iloc[:,0])
    df1.insert(loc=0,column='Players',value=l)
    radar_fig1 = radar_chart1(df1)
    st.plotly_chart(radar_fig1)
