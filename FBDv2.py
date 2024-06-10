#version 2 of the dashboard design with the inputs 8 th June
#importing necesary libraires

import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import plotly.graph_objects as go 
import plotly.express as px 
from st_aggrid import AgGrid ,GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder 

#Setting the layout

st.set_page_config(page_title='Player DashBoard',page_icon=':soccer:',
                     layout="wide")



#Loading the dataset
@st.cache_resource
def data_load ( filename):
    return pd.ExcelFile(filename)

#Data sources
#Absolute path
#"C:\Users\senth\Documents\GitHub\Pandas_practice\Data_Dashboard_Extended.xlsx"


# Player data
excel_file='Player Data2.xlsx'
# Extended data list for subbar graphs
file2='dd2.xlsx'


#Extraction
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

player_list=df['Player'].to_list()
 
#Extended data set
xl2=data_load(file2)
xl2sheets=xl2.sheet_names
#Loading of multiindex excel data
techdf=pd.read_excel(file2,sheet_name=xl2sheets[0],
                    header=[0,1])
tactdf=pd.read_excel(file2,sheet_name=xl2sheets[1],
                    header=[0,1])
#methods to get the column value of multi index data frame
#techcol=techdf.columns.get_level_values # Not required
#c=tactdf.columns.get_level_values(1) # Not required

# Assigning the player column , the frist column of the df to index and converting the tuple in index to values

techdf.set_index('Unnamed: 0_level_0', inplace=True)

techdf.index=techdf.index.map(lambda x :  x[0])

tactdf.set_index('Unnamed: 0_level_0', inplace=True)

tactdf.index=tactdf.index.map(lambda x :  x[0])

# Functions

#code for radar chart

def radar_chart1(df):
    #st.write(df) #not required
    categories=list(df.columns[1:])

    fig = go.Figure()
    config ={'scrollzoom': True}

    for i in range(df.shape[0]):
        fig.add_trace(go.Scatterpolar(
          r=list(df.iloc[i,1:]),
          theta=categories,
          fill='toself',
          name=df.iloc[i,0]
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
      
      showlegend=True
    )

    return  fig

#Function for Circle score :

def gauge(circle_score):
    fig_circle = go.Figure(go.Indicator(
    mode="gauge+number",
    value=circle_score,
    title={'text': "TSP Score",},
    gauge={
        'axis': {'range': [None, 100]},
        'bar': {'color': "black"},
        'steps': [
            {'range': [0, 50], 'color': "lightblue"},
            {'range': [50, 75], 'color': "orange"},
            {'range': [75, 100], 'color': "red"}
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

#Function fot the Bar Charts:

def bar_chart(series,name):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=series.index,
        x=list(series),
        name=name,
        orientation='h',
        text=list(series),
        textposition='inside',textangle=0,
        insidetextanchor='middle',
        textfont={'size':400},

    ))
    fig.update_layout(
        barmode='stack',
        width=1200,
        height=1200, ) #[lambda x:1800 if len(x) > 10 else 600],)
        
    
        #text=list(series))
    
    return fig

def comparison_bar_chart(series1, series2, name1,name2):
    fig = go.Figure()

    # Add trace for the first player
    fig.add_trace(go.Bar(
        y=series1.index,
        x=list(series1),
        name=name1,
        orientation='h',
        text=list(series1),
        textposition='inside',
        textangle=0,
        insidetextanchor='middle',
        textfont={'size': 30},
        marker=dict(color='blue')  # Color for the first player
    ))

    # Add trace for the second player
    fig.add_trace(go.Bar(
        y=series2.index,
        x=list(series2),
        name=name2,
        orientation='h',
        text=list(series2),
        textposition='inside',
        textangle=0,
        insidetextanchor='middle',
        textfont={'size': 30},
        marker=dict(color='orange')  # Color for the second player
    ))

    fig.update_layout(
        barmode='group',  # Use 'group' mode to place bars side-by-side
        height=1200,
        #height=lambda x:1800 if len(list(series2)) > 10 else 600,
        title='Player Comparison',
        xaxis=dict(title='Value'),
        yaxis=dict(title='Attributes')
    )

    return fig




##renaming the scores sheet for simplicity and extracting score of selected player
dfcs=circle_score_data
#circle_score = dfcs[(dfcs['Player']==selected_player)].iloc[0,1]
#st.sidebar.plotly_chart(gauge(circle_score),height=100)
#st.write(circle_score)
#st.write(selected_player)

#player selection df from the mid table area data
psdf=Mid_text_area_data

psdf['Contract']=psdf['Contract'].astype(str)
psdf['TSP Score']=(psdf['TSP Score']*100).round(0)
psdf['Age']=psdf['Age'].astype(str)

#middf.drop(9)
#selcting only the first 2 columns
psdf1=psdf[['Player','TSP Score']]


# code for AG grid display
gd=GridOptionsBuilder.from_dataframe(psdf1)
gd.configure_pagination(enabled=False)
gd.configure_selection(selection_mode='single',use_checkbox=True)

# Default player in the list to show the score when the page loads
selplayers= ['Ideal Left Winger']


# Dashboard screen starts here

st.sidebar.image('player_images/club_logo.jpg',width=100)

st.sidebar.title('Choose your player:soccer:')
with st.sidebar:
    
    stable=AgGrid(psdf1.drop(9), gridOptions=gd.build(),
                 update_mode=GridUpdateMode.SELECTION_CHANGED,
                  height=300,
                   )
# try used to by pass if there is no selection
try:
    selp2=stable['selected_rows'].iloc[0,0]
    selplayers.insert(0,selp2)
except:
    pass

# Log of the firm
st.sidebar.image('player_images/SmartScoutlogo.png',width=200)

# filtering the df with selected players
sp_details=df[df['Player'].isin(selplayers)]

#text area starts here

tdf=text_area_data
t1=tdf.columns[0] 
t2=tdf.iloc[0,0]
t3=tdf.columns[1]
t4=selplayers[0]
#t4=tdf.iloc[0,1]
#t5='TSP Score'
t6=psdf[psdf['Player']==selplayers[0]].iloc[0,5]
#st.write(t6)
#top_row=['t'+str(i) for i in range(1,6)]
#top_row=[t1,t2,t3,t4,t5,t6]
top_row=[t1,t2,t3,t4]

second_row=tdf['Primary Attributes'].tolist()
second_row.insert(0,tdf.columns[2].split()[0])

third_row=tdf[tdf.columns[3]].tolist()
third_row.insert(0,tdf.columns[3].split()[0])

#removing the nan values in the columns 4,5,6 with blank space
for i in range(4,7):
    third_row[i]=''

#fourth_row=[tdf.columns[4],tdf.iloc[0,4],tdf.columns[5],tdf.iloc[0,5]]
#replacing the coming soon with blank spaces
fourth_row=[tdf.columns[4],'18',tdf.columns[5],'7']
fifth_row=['Team Scouting For:','Sunderland A.F.C']

#list of bar for the  plot

plot_rows=[fourth_row,third_row,second_row,top_row,fifth_row]


#dynamic width for the plot 
values=[]
for i in plot_rows:
    l=[round(100/len(i),2) for j in range(len(i))]
    values.append(l)

# Normalize the values to represent percentages
normalized_values = []
for value in values:
    total = sum(value)
    percentages = [x / total * 100 for x in value]
    normalized_values.append(percentages)

# Define colors for each attribute

colors=[['lightblue','white','lightblue','white'],
        ['lightblue','white','white','white','white','white','white'],
        ['lightblue','white','white','white','white','white','white','white'],
        ['lightblue','white','white','white','white','white','white'],   
        ['lightblue','white']]#,'lightblue','white']]
# Create the figure
fig = go.Figure()
config ={'displayModeBar': False}
config ={'staticplot': True}
# Add the bar trace for each student
for i, bar_values in zip(range(5), normalized_values):
    
    for bar, percentage, color in zip(plot_rows[i], bar_values, colors[i]):
        get_font_size=lambda color: 60 if color == 'lightblue' else 20
        fig.add_trace(go.Bar(
            y=[i],  # Single bar for each row
            x=[percentage],  # The width of the segment
            name=bar,
            orientation='h',
            text=f"{bar}",#: {percentage:.1f}%",  # Text inside the bar
            textposition='inside',
            textangle=0,
            
            textfont_size=get_font_size(color),
                               
            #textfont_size=30,
            insidetextanchor='middle',  # Center-align the text inside the bars
            marker=dict(color=color),  # Set the color for each segment
            hoverinfo='none'
        ))

# Update layout
fig.update_layout(
    width=800,
    height=300,
    title={'text':'Players Dashboard ',
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

#top dahsboard chart
with col1:
       st.plotly_chart(fig,config=config)
#player image
with col2:
    if selplayers[0]=='Ideal Left Winger':
        # 'for' block is for the alignment of the image
        for i in range(6):
            st.write(' ')
        st.image('player_images/SmartScoutlogo.png',width=150)

    else:      
        pl_filename=selplayers[0].replace(' ','_')
        player_img1='player_images/'+pl_filename+'.png'        
        st.image(player_img1,width=200)
        st.subheader(selplayers[0])
        
#player Score circle plot    
with col3:
    fig2=gauge(t6)
    st.plotly_chart(fig2)

#First set of radar charts

col3, col4 = st.columns(2)




with col3:
    #st.subheader('Chart-1')
    df1=sp_details.iloc[:,:8]
    df1.drop('TSP Score',axis=1,inplace=True)
    radar_fig1 = radar_chart1(df1)
    exp=st.expander(label='Overall Attributes',expanded=False)
    config ={'displaymode': False}
    exp.plotly_chart(radar_fig1,config=config)
    
    
    
with col4:
    #st.subheader('Chart-2')
    exp=st.expander(label='Technical Attributes',expanded=False)
    colsp=sp_details.columns[8:17]
    colsp=colsp.insert(0,sp_details.columns[0])
    df=sp_details[colsp]
    
    #df=sp_details.iloc[:,8:17]
    df.columns=df.columns.str.title()
    radio_options=list(df.columns[1:])
    
    radar_fig1 = radar_chart1(df)
    exp.plotly_chart(radar_fig1,config=config)
if not selplayers[0]=='Ideal Left Winger' :
    func1=exp.radio(label='a', options=radio_options,
            label_visibility='hidden',
            horizontal=True,
            index=None )
    if func1 in radio_options :
        
        series1=techdf.loc[selplayers[0]][func1]
        series2=techdf.loc['Jack Clarke'][func1]
        #bar_data=techdf.loc[selplayers[0]][func1]
        exp3=st.expander(label='Bar chart',expanded=True)
        #exp3.plotly_chart(bar_chart((bar_data),func1))
        exp3.plotly_chart(comparison_bar_chart(series1,series2,selplayers[0],'Jack Clarke'))

    else:
        pass

# Third Row
#psdf
#st.table(middf.iloc[0:5])
midtab=psdf
midtab.set_index('Player',inplace =True)
#to round the float value in to integer
midtab['TSP Score']=psdf['TSP Score'].round().astype(int)
#to remove the decimal values in string
midtab['Age']=midtab['Age'].apply(lambda x: x.split('.')[0])

st.write(midtab.iloc[0:5],width=1)
#styled_df=midtab.iloc[0:5].style.set_table_styles(
#    [{'selector': 'th', 'props': [('background-color', 'lightgrey')]},
#    {'selector': 'table', 'props': [('width', '200%')]}]
 #   )

#html = styled_df.to_html()

# Display the styled DataFrame using st.write
#st.write(html, unsafe_allow_html=True)
col5, col6= st.columns(2)

with col5:
    #st.subheader('Chart-3')
    #df=sp_details.iloc[:,17:23]
    
    colsp=sp_details.columns[17:23]
    colsp=colsp.insert(0,sp_details.columns[0])
    df=sp_details[colsp]
    radio2_options=list(df.columns)[1:]
    #radio2_options=[x[:4] for x in radio2_options]
    #radar_fig1 = radar_chart1(df)
    #st.plotly_chart(radar_fig1)
    exp=st.expander(label='Tactical Attributes',expanded=False)
    radar_fig1 = radar_chart1(df)
    exp.plotly_chart(radar_fig1)
    
if not selplayers[0]=='Ideal Left Winger' :
    func2=exp.radio(label='a', options=radio2_options,
            label_visibility='hidden',
            horizontal=True,
            index=None )
    if func2 in radio2_options :
        
        if func2=='Team-Work':
            func2='Team-Work '
        series1=tactdf.loc[selplayers[0]][func2].round(2)
        series2=tactdf.loc['Jack Clarke'][func2].round(2)
            
        #bar_data=tactdf.loc[selplayers[0]][func2]
        #st.write(bar_data)
        exp3=st.expander(label='Bar chart',expanded=True)
        #exp3.plotly_chart(bar_chart((bar_data),func2))
        exp3.plotly_chart(comparison_bar_chart(series1,series2,selplayers[0],'Jack Clarke'))
    else:
        pass          
with col6:
    #st.subheader('Chart-4')
    df1=sp_details.iloc[:,23:]
    l=list(sp_details.iloc[:,0])
    df1.insert(loc=0,column='Players',value=l)
    exp=st.expander(label='Psychological Attributes',expanded=False)
    radar_fig1 = radar_chart1(df1)
    exp.plotly_chart(radar_fig1)
    


