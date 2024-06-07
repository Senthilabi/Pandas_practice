#version 2 of the dashboard desing with the inputs 4 th June
#importing necesary libraires
import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import plotly.graph_objects as go 
import plotly.express as px 
from st_aggrid import AgGrid ,GridUpdateMode

st.set_page_config(page_title='Player DashBoard',page_icon=':soccer:',
                     layout="wide")


#st.divider(-)
#st.write(____________)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',
             unsafe_allow_html=True)
st.title('Dashboard of players:soccer:')


#Loading the dataset

@st.cache_resource
def data_load ( filename):
    return pd.ExcelFile(filename)
excel_file='Player Data2.xlsx'
xl=data_load(excel_file)

xlsheets=xl.sheet_names

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
col=df.columns
df[col[1:]]=df[col[1:]].round(2)
df.sort_values(by=['TSP Score'],inplace=True,ascending=False)
df=df.reset_index(drop=True)
#st.table(df)
#player_list=df['Player'].to_list()
circle_score = 100
def gauge(circle_scorescore):
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
            'line': {'color': "red", 'width': 10},
            'thickness': 1,
            'value': circle_score}
        }
    ))
    return fig_circle
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        padding-top: 0px;  /* Reduce spacing from the top */
    }
    .sidebar .stPlotlyChart {
        margin-bottom: 0px;  /* Reduce spacing below the Plotly chart */
    }
    .sidebar .stMultiSelect {
        margin-top: 0px;  /* Reduce spacing above the multi-selection widget */
    }
    </style>
    """,
    unsafe_allow_html=True
)
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


st.sidebar.plotly_chart(gauge(circle_score),height=50)
st.sidebar.title('Player selection')

player_list=df['Player'].to_list()

#player_list
selected_player=st.sidebar.multiselect('Select', player_list,
                    default=player_list[0],
                    max_selections=5,key='1')

sp_details=df[(df['Player'].isin(selected_player))]
df2=Mid_text_area_data
mid_sp_details=df2[(df2['Player'].isin(selected_player))]
#st.metric
#AgGrid(mid_sp_details)
#                (df['Player']=='Ideal Left Winger' )]
#ip_details=df[df['Player']=='Ideal Left Winger']
#sp_details.drop('TSP Score',axis=1,inplace=True
#v=dfsel.iloc[0,5]

    #st.plotly_chart(fig_circle,use_container_width=True)



from st_aggrid.grid_options_builder import GridOptionsBuilder 
gd=GridOptionsBuilder.from_dataframe(mid_sp_details)
gd.configure_pagination(enabled=True)
gd.configure_selection(selection_mode='single',use_checkbox=True)
#gridoptions=gd.build()
#code for the Score card gauge

#st.sidebar.subheader(selected_player)

st.markdown(
    """
    <style>
    .custom-column {
        height: 1px;  /* Adjust the height as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)


#Text Row
c1,c2,=st.columns(2)
#c1,c11,c2,c21,c3,c31=st.columns(6)
t_c11=list(text_area_data.columns)[0]
t_v11=text_area_data.iloc[0,0]
#c11.metric(t_c11,t_v11)
#c1.subheader(t_c11+'  :')
#c11.subheader(t_v11)
t_c12=list(text_area_data.columns)[1]
t_v12=text_area_data.iloc[0,1]
#c12.metric(t_c12,t_v12)
"""
c2.subheader(t_c12+':')
c21.subheader(t_v12)
c3.subheader('Score  :')
c31.subheader(circle_score)
"""
r1heading=[t_c11,t_c12,'Score']
r1value=[t_v11,t_v12,circle_score]
dic1={x:y for x , y in zip(r1heading,r1value)}
sdf1=pd.DataFrame(dic1,columns=dic1.keys(),index=['I'])
c1.dataframe(sdf1)

#    st.markdown('<div class="custom-column">', unsafe_allow_html=True)
    
#   st.markdown('</div>', unsafe_allow_html=True)

#Text Area second row
c0,c1,c2,c3,c4,c5,c6 = st.columns([6,3,3,3,3,3,3])


t_c3=list(text_area_data.columns)[2]
t_v31=text_area_data.iloc[0,2]
t_v32=text_area_data.iloc[1,2]
t_v33=text_area_data.iloc[2,2]
t_v34=text_area_data.iloc[3,2]
t_v35=text_area_data.iloc[4,2]
t_v36=text_area_data.iloc[5,2]
t3=text_area_data[t_c3]
#c0.subheader(t_c3)
c1.write(t_v31)
c2.write(t_v32)
c3.write(t_v33)
c4.write(t_v34)
c5.write(t_v35)
c6.write(t_v36)

#c0.metric('',t_c3)

#c2.write('',t_v31)
#c2.write('',t_v32)
#c3.write('',t_v33)
#c4.write('',t_v34)
#c5.write('',t_v35)
#c6.write('',t_v36)
st.dataframe(t3.T )
c0,c1,c2,c3,c4,c5,c6 = st.columns([6,3,3,3,3,3,3])


t_c3=list(text_area_data.columns)[3]
t_v31=text_area_data.iloc[0,3]
t_v32=text_area_data.iloc[1,3]
t_v33=text_area_data.iloc[2,3]
t_v34=text_area_data.iloc[3,3]
t_v35=text_area_data.iloc[4,3]
t_v36=text_area_data.iloc[5,3]

c0.subheader(t_c3)
c1.write(t_v31)
c2.write(t_v32)
c3.write(t_v33)
c4.write(t_v34)
c5.write(t_v35)
c6.write(t_v36)
#code for the h bar plot
# Sample data
categories = ['Category 1', 'Category 2', 'Category 3','Category 4', 'Category 5']

def bar_diagram(categories):
    #categories = ['Category 1', 'Category 2', 'Category 3','Category 4', 'Category 5']
    values = [100/len(categories) for x in range(len(categories))]

    # Normalize the values to represent percentages
    total = sum(values)
    percentages = [value / total * 100 for value in values]

    # Define colors for each category
    colors = ['#636EFA', '#EF553B', '#00CC96','#FF5599','#22EEAA',
                '#234567', '#0044BB'                   ]

    # Create the figure
    fig = go.Figure()

    # Add the bar trace for each category
    for category, percentage, color in zip(categories, percentages, colors):
        fig.add_trace(go.Bar(
        y=[''],  # Single bar
        x=[percentage],  # The width of the segment
        name=category,
        orientation='h',
        text=f"{category}", #{percentage:.1f}%",  # Text inside the bar
        textposition='inside',
        textfont_size=20,
        
        marker=dict(color=color)  # Set the color for each segment
    ))

    # Update layout
    fig.update_layout(

    autosize=False,
    #    minreducedwidth=250,
    #    minreducedheight=250,
    width=600,
    height=250,
    title='',#'100% Stacked Horizontal Bar Chart',
    xaxis_title='',#'Percentage',
    yaxis_title='',
    barmode='stack',
    xaxis=dict(range=[0, 100]),  # Ensure the x-axis ranges from 0 to 100
    showlegend=False
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showline=False, showticklabels=False,linecolor='white')
    config ={'displayModeBar': False}

    return fig
#fig.update_yaxes(showline=False)
bar1=bar_diagram(categories)
# Display the chart
st.plotly_chart(bar1)

#code for hbar plot ends here
#Text 4th row
c41,c42,c43,c44=st.columns(4)
t_c41=list(text_area_data.columns)[4]
t_v41=text_area_data.iloc[0,4]
c41.subheader(t_c41+' :')
c42.write(t_v41)
t_c42=list(text_area_data.columns)[5]
t_v42=text_area_data.iloc[0,5]
c43.subheader(t_c42 +':')
c44.write(t_v42)
col3, col4 = st.columns(2)
df1=sp_details.iloc[:,1:8]
with col3:
    st.subheader('Chart-1')
    radar_fig1 = radar_chart1(df1)
    exp=st.expander(label='Click to see the chart',expanded=False)
    exp.plotly_chart(radar_fig1)
    
with col4:
    st.subheader('Chart-2')
    exp=st.expander(label='Click to see the chart',expanded=False)
    df=sp_details.iloc[:,8:18]
    radar_fig1 = radar_chart1(df)
    exp.plotly_chart(radar_fig1)

#middle table
mid_table=AgGrid(mid_sp_details, gridOptions=gd.build(),
                  update_mode=GridUpdateMode.SELECTION_CHANGED,
                  height=210,
                   )
#dfsel=mid_table['selected_rows']
#st.write(dfsel.iloc[0,0])
# Second Row
