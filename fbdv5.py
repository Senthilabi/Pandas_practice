#importing necesary libraires

import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import plotly.graph_objects as go 
import plotly.express as px 
from st_aggrid import AgGrid ,GridUpdateMode,JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder 

#Setting the layout
st.set_page_config(page_title='Profile Details',page_icon=':soccer:',
                     layout="wide")


with open('style.css') as f:
      st.markdown(f'<style> {f.read()}</style>', unsafe_allow_html=True)





#Loading the dataset
@st.cache_resource
def data_load ( filename):
    return pd.ExcelFile(filename)

#Data sources



# Player data
excel_file='Player Data2.xlsx'

#Absolute path
#"C:\Users\senth\Documents\GitHub\Pandas_practice\Data_Dashboard_Extended.xlsx"


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

Mid_text_area_data['TSP Score']=(
    Mid_text_area_data['TSP Score']*100).round(0).astype(int)

circle_score_data['TSP Score']=(
            circle_score_data['TSP Score']*100).round(0).astype(int)

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



#creating a new column in df with player name and score to display
#in sidebar mulitselect 

df['player_list']=(
    df.apply(lambda row:
         row['Player'] +'-TSP Score-'+str(row['TSP Score']),axis=1))

# Crreating a list with player name and TSP Score to displayb it in the side bar
player_list=df['player_list'].to_list()
 
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


# Assigning the player column , the frist column of the df to index and converting the tuple in index to values

techdf.set_index('Unnamed: 0_level_0', inplace=True)

techdf.index=techdf.index.map(lambda x :  x[0])

tactdf.set_index('Unnamed: 0_level_0', inplace=True)

tactdf.index=tactdf.index.map(lambda x :  x[0])
tactdf=tactdf.round(0).astype(int)



# Functions

#code for radar chart

def radar_chart1(df):
       
    categories=list(df.columns[1:])

    fig = go.Figure()
    config ={'scrollzoom': True}
    
    colors = [
        'rgba(31, 119, 180, 0.25)',  # Example color with 50% transparency
        'rgba(255, 127, 14, 0.25)',
        'rgba(44, 160, 44, 0.25)',
        'rgba(214, 39, 40, 0.25)',
        'rgba(148, 103, 189, 0.25)',
        'rgba(140, 86, 75, 0.25)',
        'rgba(227, 119, 194, 0.25)',
        'rgba(127, 127, 127, 0.25)',
        'rgba(188, 189, 34, 0.25)',
        'rgba(23, 190, 207, 0.25)'
    ]

    for i in range(df.shape[0]):
        fig.add_trace(go.Scatterpolar(
          r=list(df.iloc[i,1:]),
          theta=categories,
          fill='toself',
          fillcolor=colors[i % len(colors)],  # Cycle through colors
          line=dict(color=colors[i % len(colors)]) , # Use the same color for the line
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
      
      showlegend=True,
      legend=dict(
        orientation='h',  
        yanchor="bottom",
        y=1.1,
        xanchor="left",
        x=0.001)
          
    )

    return  fig

#Function for Circle score :

def gauge(circle_score,text):
    fig_circle = go.Figure(go.Indicator(
    mode="gauge+number",
    value=circle_score,
    #commenting the text to remove diaplay of player name
    #title={'text': text+" TSP ",},
    title={'text': " TSP ",},       
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
        textfont={'size':40},

    ))
    fig.update_layout(

        barmode='stack',
        width=1200,
        height=1200, 
        font=dict(size=40)), #[lambda x:1800 if len(x) > 10 else 600],)
        
    
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

def multiPle_bar_chart(df,player):
    barplayer=player
    mpdf=df.loc[barplayer]
    c=list(mpdf.columns)
    a=len(c)
    b=len(barplayer)
    #st.write(a)
    #st.write(len(a))
    ab=a*b
    if ab < 15:
        h=300
    elif ab < 30:
        h=600
    elif ab < 45:
        h=1200
    elif ab < 60:
        h=1800
    elif ab < 75:
        h=2500
    else:
        h=3600

    fig = go.Figure()
    for i in range((mpdf.shape[0])):
        series=mpdf.iloc[i,1:]
        name=barplayer[i]
        #name='Series'
        

        # Add trace for the first player
        fig.add_trace(go.Bar(
            y=series.index,
            x=list(series),
            name=name,
            orientation='h',
            text=list(series),
            textposition='outside', #inside
            textangle=0,
            insidetextanchor='middle',
            textfont={'size': 15},
            #marker=dict(color='blue')  # Color for the first player
        ))
    fig.update_layout(
        barmode='group',  # Use 'group' mode to place bars side-by-side
        height=h,
        bargap=0.1,bargroupgap=.3,
        #height=lambda x:1800 if len(list(series2)) > 10 else 600,
        title='Player Comparison',
        xaxis=dict(title='Value'),
        yaxis=dict(title='Attributes'),
        font=dict(size=30,color='Rebecca Purple')
    )
    return fig

def table_plot(df,title=None,height=150,width=500,heading_color='black',row_color='lightblue') :
    height= 200+50*(df.shape[0])
    cell_text=df.values.tolist()
    col_width= round(100/df.shape[1],2)
    col_header=df.columns.tolist()
    cell_text.insert(0,col_header)
    cell_text=list(reversed(cell_text))
    rows=len(cell_text)
    fig = go.Figure()
    config ={'displayModeBar': False}
    config ={'staticplot': True}
    for row in range(rows):
        get_color= lambda row : heading_color if row ==(rows-1) else row_color
        for text in cell_text[row]:
            
            fig.add_trace(go.Bar
                         (
                         #y=list(range(rows)),
                         y=[row] ,  
                         x=[col_width],
                         name=text,
                         orientation='h',
                             
                    
                         text=f'{text}',
                         textposition='inside',
                         textangle=0,
                         insidetextanchor='middle',
                         marker_line_width=1,
                         marker=dict(color=get_color(row)),   
                         hoverinfo='none'


                         ) )
    # Update layout
    fig.update_layout(
        width=width,
        height=height,
        title={'text':title,
                'font': {
                'family': "Courier New, monospace",
                'size': 20,
                'color': "RebeccaPurple"}

        },
        #xaxis_title='Percentage',
        #yaxis_title='',
        barmode='stack',
        bargap=0.,bargroupgap=0.1,
        xaxis=dict(range=[0, 100]),  # Ensure the x-axis ranges from 0 to 100
        showlegend=False,

    )
    fig.update_xaxes(showticklabels=False,linecolor='white')
    fig.update_yaxes(showline=False, showticklabels=False,linecolor='white')
    return fig

#fig.update_layout(barmode='group', bargap=0.30,bargroupgap=0.0)

def display_label(name,height=300,width=300,thick=3):
    fig = go.Figure()
    config ={'staticplot': True}
    config ={'displayModeBar': False}
    fig.add_traces(go.Bar(x=[1],y=[1],orientation='h',text=name,insidetextanchor='middle',marker_line_width=thick, 
                         textposition='inside',textangle=0,hoverinfo='none'))
    fig.update_layout(width=width,height=height,barmode='stack')
    #        xaxis=dict(range=[0, 100]))
    fig.update_xaxes(showticklabels=False,linecolor='white')
    fig.update_yaxes(showline=False, showticklabels=False,linecolor='white')
    config ={'displayModeBar': False}

    return fig


##renaming the scores sheet for simplicity and extracting score of selected player
dfcs=circle_score_data

#player selection df from the mid table area data
psdf=Mid_text_area_data

psdf['Contract']=psdf['Contract'].astype(str)
#psdf['TSP Score']=(psdf['TSP Score']).round(0)
psdf['Age']=psdf['Age'].astype(str)

#middf.drop(9)
#selcting only the first 2 columns
psdf1=psdf[['Player','TSP Score']]


#1

# Dashboard screen starts here

#"C:\Users\senth\Documents\GitHub\Pandas_practice\player_images\Sunderland..png"
#columns option not working in side bar


st.sidebar.image('player_images/Sunderland..png',width=100)

st.sidebar.title('Choose your player  '+'   :soccer:')
try:
    selplayerbar =st.sidebar.multiselect(label='Select players',
            options=player_list[1:],label_visibility='hidden',
            max_selections=5
            )
    
    
    
except:
    
    pass

selplayerbar.append(df['player_list'][0]) # adding Ideal player  as  default in the selection for radar charts
#slicing the df to have only the details of selected players
selplayerdf=df[df['player_list'].isin(selplayerbar)] # Player_list is a combination of playername and Tsp score

selplayers=selplayerdf['Player'].tolist()


# Logo of the firm
#st.sidebar.image('player_images/SmartScoutlogo.png',width=200)


sp_details=selplayerdf

#text area starts here

tdf=text_area_data
t1=tdf.columns[0] 
t2=tdf.iloc[0,0]
t3=tdf.columns[1]
if len(selplayers)>1 :
    t4=selplayers[1]
else:
    t4=selplayers[0]


#t5='TSP Score'
#t6=psdf[psdf['Player']==selplayers[0]].iloc[0,5]
t6=psdf[psdf['Player']==t4].iloc[0,5]
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
        ['lightblue','white','lightblue','white','white','white','white'],   
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
            marker_line_width=1,
            hoverinfo='none'
        ))

# Update layout
fig.update_layout(
    width=700,
    height=350,
    title={'text':'Profile Details ',
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
#col1 ,col2, col3 =st1.columns([3,1,1])
col1,col3=st1.columns([4,1])
#top dahsboard chart
with col1:

       st.plotly_chart(fig,config=config)
#player image
#with col2:
#    for i in range(6):
#            st.write(' ')
#        
#    st.image('player_images/SmartScoutlogo.png',width=150)

        
#player Score circle plot    
with col3:
    #st.write(selplayers[0])
    fig2=gauge(t6,t4)
    st.plotly_chart(fig2)
    
#code for the image display

if   (len(selplayers) >1):
    display_players=selplayers[1:]
    l=len(display_players)
    pic_cols=['col1','col2','col3','col4','col5']
    pic_cols[:l]=st1.columns(l)
    if l==1:
        pic_cols[:2]=st1.columns([1,3]) 
    if l==2:
        
        pic_cols[:3]=st1.columns([1,1,2])
        
    #code for concating the player name with file extension to retireive the file from the image folder
    for i in range(l):
      
        pl_filename=display_players[i].replace(' ','_')       
        player_img1='player_images/'+pl_filename+'.png'        
        pic_cols[i].image(player_img1,width=100)
        pic_cols[i].subheader(display_players[i])
    if l==2:
        calldf=sp_details.iloc[:,8:-1]
        calldf=calldf.drop(0)
        calldf=calldf.reset_index()
        
        
        #finding differences
        call=calldf.diff(axis=0)
        
        allsimilar=[]
        allfirst=[]
        allsecond=[]
        
        
        
        for i in call.columns:
            
            val=(call[i])[1]
            if abs(val) <= 10:
                allsimilar.append(i)
            elif val < -10:
                allfirst.append(i)
            else:
                allsecond.append(i)
        #calldict={'Players':display_players}
        
        #st.write(call)
        sim=len(allsimilar)
        pl_f=len(allfirst)
        pl_s=len(allsecond)
        pl_f_points=sim*2+pl_f*5
        pl_s_points=sim*2+pl_s*5
        calldict={}
        calldict[display_players[0]]=[pl_f_points,pl_f,sim,pl_s,]
        calldict[display_players[1]]=[pl_s_points,pl_s,sim,pl_f]
        dfcomptop=pd.DataFrame(calldict,index=['Points','Won','Draw','Lost',]).T
        dfcomptop.reset_index(inplace=True)
        dfcomptop.rename({'index':'Players'},axis=1, inplace=True)
        #st.write(list(dfcomptop.columns))
        
        #pic_cols[2].table(pd.DataFrame(calldict,index=['Points','Won','Draw','Lost',]).T)
        pic_cols[2].plotly_chart(table_plot(dfcomptop,title='Attribute Comparison'))


    
    
    
#details for counter chart        
#radardf1=sp_details.iloc[:,:8]
calldf=sp_details.iloc[:,8:-1]
calldf=calldf.drop(0)
#calldf.columns=map(str.title,calldf.columns)
#st.write(calldf)
cpsychdf=sp_details.iloc[:,23:-1]
#Dropping the Ideal player
cpsychdf=cpsychdf.drop(0)
ctechdf=sp_details.iloc[:,8:17]

ctechdf=ctechdf.drop(0)
ctechdf.columns=map(str.title,ctechdf.columns)

ctactdf=sp_details.iloc[:,17:23]
ctactdf=ctactdf.drop(0)

#st.write(cpsychdf)
#st.write(ctechdf)
#st.write(ctactdf)

# Third Row
#psdf
#st.table(middf.iloc[0:5])
midtab=psdf
midtab['TSP Score']=psdf['TSP Score'].round().astype(int)
midtab=midtab[midtab['Player'].isin(selplayers)]
midtab.set_index('Player',inplace =True)
#to round the float value in to integer

#to remove the decimal values in string
midtab['Age']=midtab['Age'].apply(lambda x: x.split('.')[0])

if not midtab.shape[0]==1 :
    mid_table=midtab.iloc[:-1]
    mid_table= mid_table.reset_index()
    st.plotly_chart(table_plot(mid_table, width=1200, title='Player Profile'))
    #st.write(midtab.iloc[:-1])
       
    
    
    
#styled_df=midtab.iloc[0:5].style.set_table_styles(
#    [{'selector': 'th', 'props': [('background-color', 'lightgrey')]},
#    {'selector': 'table', 'props': [('width', '200%')]}]
 #   )

#html = styled_df.to_html()

# Display the styled DataFrame using st.write
#st.write(html, unsafe_allow_html=True)


#First set of radar charts
col3, col4 = st.columns(2)




with col3:
    #st.subheader('radar Chart-1')
    radardf1=sp_details.iloc[:,:8]
    radardf1.drop('TSP Score',axis=1,inplace=True)
    radar_fig1 = radar_chart1(radardf1)
    exp=st.expander(label='Overall Attributes',expanded=False)
    config ={'displaymode': False}
    exp.plotly_chart(radar_fig1,config=config)
    
    
    
with col4:
    #st.subheader('radar Chart-2')
    radardf2=sp_details.iloc[:,23:-1]
    l=list(sp_details.iloc[:,0])
    radardf2.insert(loc=0,column='Players',value=l)
    exp=st.expander(label='Psychological Attributes',expanded=False)
    radar_fig2 = radar_chart1(radardf2)
    exp.plotly_chart(radar_fig2)
    
col5, col6= st.columns(2)

with col5:
    #st.subheader('radar Chart-3')
    exp=st.expander(label='Technical Attributes',expanded=False)
    colsp1=sp_details.columns[8:17]
    colsp1=colsp1.insert(0,sp_details.columns[0])
    radardf3=sp_details[colsp1]
    
    #df=sp_details.iloc[:,8:17]
    radardf3.columns=radardf3.columns.str.title()
    radio_options=list(radardf3.columns[1:])
    
    radar_fig3 = radar_chart1(radardf3)
    exp.plotly_chart(radar_fig3,config=config)
#if not selplayers[0]=='Ideal Left Winger' :
if len(selplayers) >1 :
    bar1players=selplayers[1:]
    
    expr1=st.expander(label=' More on Technical Attributes ',expanded=False)
    func1=expr1.radio(label='a', options=radio_options,
            label_visibility='hidden',
            horizontal=True,
            index=None )
    if func1 in radio_options :
        
        if not 'Jack Clarke' in bar1players:
            bar1players.append('Jack Clarke')
             
        techdf1=techdf.loc[bar1players][func1]
        
        exp3=st.expander(label='Bar chart',expanded=True)
        
        exp3.plotly_chart(multiPle_bar_chart(techdf1,bar1players))
        pass
with col6:
    #st.subheader('Chart-4')
    #df=sp_details.iloc[:,17:23]
    
    colsp2=sp_details.columns[17:23]
    colsp2=colsp2.insert(0,sp_details.columns[0])
    radardf4=sp_details[colsp2]
    radio2_options=list(radardf4.columns)[1:]
    
    exp=st.expander(label='Tactical Attributes',expanded=False)
    radar_fig4 = radar_chart1(radardf4)
    exp.plotly_chart(radar_fig4)
    
#if not selplayers[0]=='Ideal Left Winger' :
if len(selplayers) >1 :
    bar2players=selplayers[1:]
    
    expr1=st.expander(label=' More on Tactical Attributes ',expanded=False)
    func2=expr1.radio(label='a', options=radio2_options,
            label_visibility='hidden',
            horizontal=True,
            index=None )
    if func2 in radio2_options :
        
        if func2=='Team-Work':
            func2='Team-Work '
        
        if not 'Jack Clarke' in bar2players:
            
            bar2players.append('Jack Clarke')
        
        #selplayers=selplayers[1:]
        
        tactdf1=tactdf[func2].loc[bar2players]    
        
        exp3=st.expander(label='Bar chart',expanded=True)
        
        exp3.plotly_chart(multiPle_bar_chart(tactdf1,bar2players))
    else:
        pass  
    
#if  (len(selplayers) ==3):
        
#        st.write(tactdf1)
 
#code for counter starts here


try:
    if  (len(display_players) ==2):
        #creating a newdf for comapriaosn with only players visible in the image section
        techdfcomp=techdf[func1].loc[display_players]
        techdfcomp.reset_index(inplace=True)
         
        
        cltech=list(techdfcomp.columns)
        cltech[0]='Players'
        
        techdfcomp.columns=cltech
        techdfcomp.set_index('Players',inplace=True)
        
        #finding differences
        ltech=techdfcomp.diff(axis=0)
        
        
        similar1=[]
        first1=[]
        second1=[]
        
        
        for i_t in ltech.columns:
            
            val=ltech[i_t][1]
            if abs(val) <=10:
                similar1.append(i_t)
            elif val < -10:
                first1.append(i_t)
            else:
                second1.append(i_t)
        st.sidebar.subheader('Comparison on '+ func1) 
            
        similartechdf=techdfcomp[similar1]
    
        first_player1=list(techdfcomp.index)[0]
        second_player1=list(techdfcomp.index)[1]
        
        #comparison_dict2 ={'Similar Attributes':similartechdf.shape[1],(first_player1 +' Won') :techdfcomp[first1].shape[1],
        #                 (second_player1 +' Won'):techdfcomp[second1].shape[1]} 

#comparison_dict2 ={'Similar Attributes':similartechdf.shape[1],(first_player1 +' Won') :techdfcomp[first1].shape[1],
#                     (second_player +' Won'):techdfcomp[second1].shape[1]} 
#comparison_dict
        
        points_first1=techdfcomp[first1].shape[1]*5+similartechdf.shape[1]*2
        points_second1=techdfcomp[second1].shape[1]*5+similartechdf.shape[1]*2
        comparison_dict2={'Players':[first_player1,second_player1],'Points':[points_first1,points_second1],
                          'Won':[techdfcomp[first1].shape[1],techdfcomp[second1].shape[1]],
                          'Draws':[similartechdf.shape[1],similartechdf.shape[1]],
                          'Loss':[techdfcomp[second1].shape[1],techdfcomp[first1].shape[1]]}
        compsidedf2=pd.DataFrame(comparison_dict2, columns=comparison_dict2.keys())#,index=[func1])
        compsidedf2.set_index('Players',inplace=True)

        st.sidebar.table(compsidedf2) 
 
                                                                        

    
            
except:
    pass


try:
    if  (len(display_players) ==2):
        #creating a newdf for comapriaosn with only players visible in the image section
        tactdfcomp=tactdf[func2].loc[display_players]
        tactdfcomp.reset_index(inplace=True)
        
        cl=list(tactdfcomp.columns)
        cl[0]='Players'
        
        tactdfcomp.columns=cl
        tactdfcomp.set_index('Players',inplace=True)
        
        #finding differences
        l=tactdfcomp.diff(axis=0)
        
        similar=[]
        first=[]
        second=[]
        
        
        for i in l.columns:
            
            val=l[i][1]
            if abs(val) <=10:
                similar.append(i)
            elif val < -10:
                first.append(i)
            else:
                second.append(i)
        st.sidebar.subheader('Comparison on '+ func2) 
       # comparison_dict ={'Similar Attributes':similardf.shape[1],(first_player +' Won') :tactdfcomp[first].shape[1]
                         # (second_player +' Won'):tactdfcomp[second].shape[1}
        #st.sidebar.subheader('Similar Attributes')
        similartactdf=tactdfcomp[similar]
        #st.sidebar.write(similardf.shape[1])
        first_player=list(tactdfcomp.index)[0]
        #st.sidebar.subheader(first_player +' Won')
        #st.sidebar.write(tactdfcomp[first].shape[1])
        second_player=list(tactdfcomp.index)[1]
        #st.sidebar.subheader(second_player +' Won')
        #st.sidebar.write(tactdfcomp[second].shape[1])
        #comparison_dict ={'Similar Attributes':similardf.shape[1],(first_player +' Won') :tactdfcomp[first].shape[1],
                          #(second_player +' Won'):tactdfcomp[second].shape[1]} 
        #compsidedf=pd.DataFrame(comparison_dict, columns=comparison_dict.keys)

        #comparison_dict ={'Similar Attributes':similartactdf.shape[1],(first_player +' Won') :tactdfcomp[first].shape[1],
                         #(second_player +' Won'):tactdfcomp[second].shape[1]} 
        #comparison_dict

        #compsidedf=pd.DataFrame(comparison_dict, columns=comparison_dict.keys(),index=[func2])
        #st.sidebar.write(compsidedf.T)
        #st.sidebar.write(compsidedf.T)
        points_first=tactdfcomp[first].shape[1]*5+similartactdf.shape[1]*2
        points_second=tactdfcomp[second].shape[1]*5+similartactdf.shape[1]*2
        comparison_dict={'Players':[first_player,second_player],'Points':[points_first,points_second],
                          'Won':[tactdfcomp[first].shape[1],tactdfcomp[second].shape[1]],
                          'Draws':[similartactdf.shape[1],similartactdf.shape[1]],
                          'Loss':[tactdfcomp[second].shape[1],tactdfcomp[first].shape[1]]}
        compsidedf=pd.DataFrame(comparison_dict, columns=comparison_dict.keys())#,index=[func1])
        compsidedf.set_index('Players',inplace=True)

        st.sidebar.table(compsidedf) 


            
except:
    pass
try:
    

    

    bothcompdf=compsidedf2.T.merge(compsidedf.T , left_index=True, right_index=True)
    #st.sidebar.write(bothcompdf)
except:
    pass

