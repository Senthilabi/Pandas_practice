#version 2 of the dashboard desing with the inputs 6 th June
#importing necesary libraires

import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import plotly.graph_objects as go 
import plotly.express as px 
from st_aggrid import AgGrid ,GridUpdateMode

#Setting the layout

st.set_page_config(page_title='Player DashBoard',page_icon=':soccer:',
                     layout="wide")



#Loading the dataset
#import base64

#@st.cache_data()
#def get_base64_of_bin_file(bin_file):
#    with open(bin_file, 'rb') as f:
#        data = f.read()
#    return base64.b64encode(data).decode()

#def set_png_as_page_bg(png_file):
#    bin_str = get_base64_of_bin_file(png_file)
#   page_bg_img = '''
#    <style>
#    body {
#    background-image: url("data:image/png;base64,%s");
#    background-size: cover;
#    }
#    </style>
#    ''' % bin_str
#    #st.write('Hello inside ')
#    st.markdown(page_bg_img, unsafe_allow_html=True)
#    return
#bgfile='player_images/Bruma.png'
#set_png_as_page_bg(bgfile)

@st.cache_resource
def data_load ( filename):
    return pd.ExcelFile(filename)
excel_file='Player Data2.xlsx'
xl=data_load(excel_file)

xlsheets=xl.sheet_names
#Extracting the indiviual sheet to DF
text_area_data = pd.read_excel(excel_file, sheet_name=xlsheets[0])
circle_score_data = pd.read_excel(excel_file, sheet_name=xlsheets[1])
radar_chart1_data = pd.read_excel(excel_file, sheet_name=xlsheets[2])
radar_chart2_data = pd.read_excel(excel_file, sheet_name=xlsheets[3])
radar_chart3_data = pd.read_excel(excel_file, sheet_name=xlsheets[5])
radar_chart4_data = pd.read_excel(excel_file, sheet_name=xlsheets[6])
Mid_text_area_data = pd.read_excel(excel_file, sheet_name=xlsheets[4])

# Converting the score from decimal to %
circle_score_data['TSP Score']=circle_score_data['TSP Score']*100

#Merging the data
df=circle_score_data.merge(radar_chart1_data, how ='outer',on='Player')

df=df.merge(radar_chart2_data, how ='outer',on='Player')
df=df.merge(radar_chart3_data,how='outer',on='Player')
df=df.merge(radar_chart4_data,how='outer',on='Player')
col=df.columns

# rounding  of the decimals to 2 places and sorting
df[col[1:]]=df[col[1:]].round(2)
df.sort_values(by=['TSP Score'],inplace=True,ascending=False)
df=df.reset_index(drop=True)
#st.write(df.columns)
#st.table(df)
player_list=df['Player'].to_list()
 
file2='Data_Dashboard_Extended.xlsx'
#"C:\Users\senth\Documents\GitHub\Pandas_practice\Data_Dashboard_Extended.xlsx"
xl2=data_load(file2)
xl2sheets=xl2.sheet_names
techdf=pd.read_excel(file2,sheet_name=xl2sheets[0],
                    header=[0,1])
tactdf=pd.read_excel(file2,sheet_name=xl2sheets[1],
                    header=[0,1])
techcol=techdf.columns.get_level_values
c=tactdf.columns.get_level_values(1)
techdf.set_index('Unnamed: 0_level_0', inplace=True)

techdf.index=techdf.index.map(lambda x :  x[0])

tactdf.set_index('Unnamed: 0_level_0', inplace=True)

tactdf.index=tactdf.index.map(lambda x :  x[0])
#st.write(tactdf.index)
#code for radar chart

def radar_chart1(df2):

    categories=list(df2.columns[1:])

    fig = go.Figure()
    config ={'scrollzoom': True}

    for i in range(df2.shape[0]):
        fig.add_trace(go.Scatterpolar(
          r=list(df2.iloc[i,1:]),
          theta=categories,
          fill='toself',
          name=df2.iloc[i,0]
    ))
    fig.update_layout(
      height=500,
      width=500,
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 100]
        ),
      ),
      
      showlegend=False
    )

    return  fig



#renaming the scores sheet for simplicity and extracting score of selected player
dfcs=circle_score_data
#circle_score = dfcs[(dfcs['Player']==selected_player)].iloc[0,1]
#st.sidebar.plotly_chart(gauge(circle_score),height=100)
#st.write(circle_score)
#st.write(selected_player)
# CSS Code for changing the alignment of score card , but no effect
st.sidebar.markdown(
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
def gauge(circle_score):
    fig_circle = go.Figure(go.Indicator(
    mode="gauge+number",
    value=circle_score,
    title={'text': "TSP Score",},
    gauge={
        'axis': {'range': [None, 100]},
        'bar': {'color': "darkred"},
        'steps': [
            {'range': [0, 50], 'color': "lightgoldenrodyellow"},
            {'range': [50, 75], 'color': "orange"},
            {'range': [75, 100], 'color': "darkorange"}
        ],
        'threshold': {
            'line': {'color': "black", 'width': 10},
            'thickness': 1,
            'value': circle_score}
        }
     
        
    ))
    fig_circle.update_layout(
    width=800,
    height=300)
    return fig_circle
def bar_chart(series,name):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=series.index,
        x=list(series),
        name=name,
        orientation='h',

    ))
    fig.update_layout(barmode='stack')
    return fig


middf=Mid_text_area_data
middf['Contract']=middf['Contract'].astype(str)
middf['TSP Score']=(middf['TSP Score']*100).round(0)
middf['Age']=middf['Age'].astype(str)
#middf.drop(9)
middf1=middf[['Player','TSP Score']]


from st_aggrid.grid_options_builder import GridOptionsBuilder 
gd=GridOptionsBuilder.from_dataframe(middf1)
gd.configure_pagination(enabled=False)
gd.configure_selection(selection_mode='single',use_checkbox=True)
selplayers= ['Ideal Left Winger']

st.sidebar.title('Choose your player:soccer:')
with st.sidebar:
    #st.sidebar.subheader(selected_player)
    mid_table=AgGrid(middf1.drop(9), gridOptions=gd.build(),
                 update_mode=GridUpdateMode.SELECTION_CHANGED,
                  height=400,
                   )

try:
    selp2=mid_table['selected_rows'].iloc[0,0]
    selplayers.insert(0,selp2)
except:
    pass
#selplayers.append(selp2)

st.sidebar.image('player_images/SmartScoutlogo.png',width=200)
sp_details=df[df['Player'].isin(selplayers)]
#text area starts here
tdf=text_area_data
t1=tdf.columns[0]
t2=tdf.iloc[0,0]
t3=tdf.columns[1]
t4=selplayers[0]
#t4=tdf.iloc[0,1]
t5='TSP Score'
t6=middf[middf['Player']==selplayers[0]].iloc[0,5]
#st.write(t6)
#top_row=['t'+str(i) for i in range(1,6)]
#top_row=[t1,t2,t3,t4,t5,t6]
top_row=[t1,t2,t3,t4]

second_row=tdf['Primary Attributes'].tolist()
second_row.insert(0,tdf.columns[2].split()[0])

third_row=tdf[tdf.columns[3]].tolist()
third_row.insert(0,tdf.columns[3].split()[0])
for i in range(4,7):
    third_row[i]=''

fourth_row=[tdf.columns[4],tdf.iloc[0,4],tdf.columns[5],tdf.iloc[0,5]]

plot_rows=[fourth_row,third_row,second_row,top_row]

values=[]
for i in plot_rows:
    l=[round(100/len(i),2) for j in range(len(i))]
    values.append(l)

# Normalize the values to represent percentages
normalized_values = []
for student_values in values:
    total = sum(student_values)
    percentages = [value / total * 100 for value in student_values]
    normalized_values.append(percentages)

# Define colors for each attribute
#colors = ['#636EFA', '#EF553B', '#00CC96','#112277','#225577','#004488','#2266AA']
colors=[['lightblue','white','lightblue','white','lightblue','white'],
        ['black','darkorange','darkorange','darkorange','darkorange','darkorange','darkorange'],
                    ['black','darkorange','darkorange','darkorange','darkorange','darkorange','darkorange'],   ['lightblue','white','lightblue','white','lightblue','white']]
# Create the figure
fig = go.Figure()
config ={'displayModeBar': False}
config ={'staticplot': True}
# Add the bar trace for each student
for i, bar_values in zip(range(4), normalized_values):
    
    for bar, percentage, color in zip(plot_rows[i], bar_values, colors[i]):
        
        fig.add_trace(go.Bar(
            y=[i],  # Single bar for each row
            x=[percentage],  # The width of the segment
            name=bar,
            orientation='h',
            text=f"{bar}",#: {percentage:.1f}%",  # Text inside the bar
            textposition='inside',
            textfont_size=30,
            insidetextanchor='middle',  # Center-align the text inside the bars
            marker=dict(color=color),  # Set the color for each segment
            hoverinfo='none'
        ))

# Update layout
fig.update_layout(
    width=800,
    height=300,
    title={'text':'Players Dashboard',
            'font': {
            'family': "Courier New, monospace",
            'size': 30,
            'color': "RebeccaPurple"}
    
    },
    #xaxis_title='Percentage',
    #yaxis_title='',
    barmode='stack',
    xaxis=dict(range=[0, 100]),  # Ensure the x-axis ranges from 0 to 100
    showlegend=False,
    
)
fig.update_xaxes(showticklabels=False,linecolor='white')
fig.update_yaxes(showline=False, showticklabels=False,linecolor='black')
config ={'displayModeBar': False}

# Display the chart
st1=st.expander(label='',expanded=True)
col1 ,col2, col3 =st1.columns([3,1,1])
with col1:
       st.plotly_chart(fig,config=config)

with col2:
    if selplayers[0]=='Ideal Left Winger':
        for i in range(6):
            st.write(' ')
        st.image('player_images/SmartScoutlogo.png',width=150)

    else:      
        pl_filename=selplayers[0].replace(' ','_')
        player_img1='player_images/'+pl_filename+'.png'
        #player_img='player_images/Andreas_S_Olsen.png'
        #st.write(player_img)
        #st.write(player_img1)
        #from PIL import Image
        #input_image = Image.open(player_img1)
        #st.image(input_image,width=200)
        #st.image('player_images/Antonia_Nusa.png',width=200)
        st.image(player_img1,width=200)

        st.subheader(selplayers[0])
with col3:
    fig2=gauge(t6)
    st.plotly_chart(fig2)

col3, col4 = st.columns(2)
df1=sp_details.iloc[:,1:8]
with col3:
    #st.subheader('Chart-1')
    radar_fig1 = radar_chart1(df1)
    exp=st.expander(label='Overall Attributes',expanded=False)
    config ={'displaymode': False}
    exp.plotly_chart(radar_fig1,config=config)
    
    
    
with col4:
    #st.subheader('Chart-2')
    exp=st.expander(label='Overall Technical',expanded=False)
    df=sp_details.iloc[:,8:17]
    df.columns=df.columns.str.title()
    radio_options=list(df.columns)
    #radio_options=[x[:5] for x in radio_options]
    #radio_options=[x.title() for x in radio_options]
    radar_fig1 = radar_chart1(df)
    exp.plotly_chart(radar_fig1,config=config)
    if not selplayers[0]=='Ideal Left Winger' :
        func1=exp.radio(label='a', options=radio_options,
                label_visibility='hidden',
                horizontal=True,
                index=None )
        if func1 in radio_options :
            #st.write(func1)
            #st.write(selplayers[0])
            #st.write(techdf.loc[selplayers[0]],[func1])
            #st.write(techdf)
            
            bar_data=techdf.loc[selplayers[0]][func1]
            #st.write(bar_data)
            exp2=st.expander(label='Bar chart',expanded=True)
            exp2.plotly_chart(bar_chart((bar_data),func1))
        else:
            pass
#middle table

#dfsel=mid_table['selected_rows']
#st.write(dfsel.iloc[0,0])
# Second Row
# Third Row
middf['TSP Score']=middf['TSP Score'].astype(str)
#st.table(middf.iloc[0:5])
midtab=middf
midtab.set_index('Player',inplace =True)
st.table(midtab.iloc[0:5])
col5, col6= st.columns(2)

with col5:
    #st.subheader('Chart-3')
    df=sp_details.iloc[:,17:25]
    radio2_options=list(df.columns)[1:]
    #radio2_options=[x[:4] for x in radio2_options]
    #radar_fig1 = radar_chart1(df)
    #st.plotly_chart(radar_fig1)
    exp=st.expander(label='Overall Tactical',expanded=False)
    radar_fig1 = radar_chart1(df)
    exp.plotly_chart(radar_fig1)
    
    if not selplayers[0]=='Ideal Left Winger' :
        func2=exp.radio(label='a', options=radio2_options,
                label_visibility='hidden',
                horizontal=True,
                index=None )
        if func2 in radio2_options :
            #st.write(func1)
            #st.write(selplayers[0])
            #st.write(techdf.loc[selplayers[0]],[func1])
            #st.write(techdf)
            
                
            bar_data=tactdf.loc[selplayers[0]][func2]
            #st.write(bar_data)
            exp2=st.expander(label='Bar chart',expanded=True)
            exp2.plotly_chart(bar_chart((bar_data),func2))
        else:
            pass          
with col6:
    #st.subheader('Chart-4')
    df1=sp_details.iloc[:,25:]
    l=list(sp_details.iloc[:,0])
    df1.insert(loc=0,column='Players',value=l)
    exp=st.expander(label='Overall Psychological',expanded=False)
    radar_fig1 = radar_chart1(df1)
    exp.plotly_chart(radar_fig1)

