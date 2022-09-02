from fileinput import filename
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from google.oauth2 import service_account
from gsheetsdb import connect
import scipy as sp
import pingouin as pg
import pickle
import regex as re

# Data fetching from Google Sheets
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Data proccesing
data = pd.DataFrame(rows)
data['district'] =data['district'].str.replace(" ","")
data['Year'] = data['Year'].astype(str) 
data['Year'] = data['Year'].str.slice(0,-2)
data['Price'] = data['Price'].astype(float)
data['Space'] = data['Space'].astype(float)
sample = data.sample(n=750, random_state=42)

data.replace({'elevatoe': {1: 'jest', 0: 'nie ma'}}, inplace=True)
data.replace({'Parkingplace': {1: 'jest', 0: 'nie ma'}}, inplace=True)
data.replace({'balkon': {1: 'jest', 0: 'nie ma'}}, inplace=True)
data.replace({'taras': {1: 'jest', 0: 'nie ma'}}, inplace=True)
data.replace({'ogrdek': {1: 'jest', 0: 'nie ma'}}, inplace=True)

st.sidebar.subheader('Data Exploration')
st.sidebar.subheader('Factors that mostly influeces price')
st.sidebar.subheader('Analysis in depth of couple districs')
st.sidebar.subheader('Price prediction model based on proviede data')
    
st.title('Warsaw flats prices in July of 2022')
st.markdown("""This is a small data science report about real estate market in Warsaw. This dataset was made purely my me. I have scrapped flats offers from Otodomo page.
            Dataset consist of 15 columns.\\
            Thing you can find in the report: \\
            - Dataset reiview \\
            - Factors that mostly influece price \\
            - Analysis in depth of couple districs \\
            - Model predicting price of a flat based on provided features
            
""")



st.header("Data Exploration")
"""This is real world data about estates market in Warsaw. There are 15 columns. Two features are two continous variables and the rest are categorical - 13. """
st.write(data.head(20))
"""Distribution of rooms in the dataset. Since the dataset is huge I have sampled it to see the distribution of rooms. """
def rooms_distribution_plot():
    plt.style.use('ggplot')
    fig= plt.figure(figsize=(19,10))
    fig.suptitle('Distribution of rooms column', fontsize=25)
    plt.xlabel('Rooms', fontsize=25);
    plt.ylabel('Count', fontsize=25);
    plt.xticks([0,1,2,3,4,5,6,7,8,9],fontsize=20);
    fig.tight_layout()
    sns.histplot(sample, x ='Rooms', discrete=True)
    return st.pyplot(fig)

rooms_distribution_plot()
f"""Most flats have two or three rooms. Kurtosis is {round(sp.stats.kurtosis(data.Rooms), 2 )}, and skewness is {round(sp.stats.skew(data.Rooms), 2 )}. """



st.header("Factors that mostly influeces price")
f"""The most important factors that influence price are:"""
st.table(sample.corr()['Price'].sort_values(ascending=False)[1:4])

#Rooms and Price
#{round(pg.anova(data= sample , dv = 'Price', between='Rooms')['p-unc'].values[0],30)}
"""#### Rooms and Price realtionship"""
fig1= plt.figure(figsize=(19,10))
fig1.suptitle('Boxplots of Rooms by Price', fontsize=25)
plt.xlabel('Rooms', fontsize=25);
plt.ylabel('Price', fontsize=25);
sns.boxplot(data=sample, x='Rooms', y='Price')
st.pyplot(fig1)
f"""ANOVA realtionship beetwen rooms and price is statisticlly significant p-value is smaller than 0.05,
and eta sqaured effect is equal to = {round(pg.anova(data= sample , dv = 'Price', between='Rooms')['np2'].values[0],3)}. """
st.table(data.groupby('Rooms')['Price'].agg([np.mean,np.std,np.median][:5]))


#Space and Price
"""#### Space and Price realtionship"""
fig2= plt.figure(figsize=(19,10))
fig2.suptitle('Space and Price scatter plot', fontsize=25)
plt.xlabel('Space', fontsize=25);
plt.ylabel('Price', fontsize=25);
sns.scatterplot(data=sample, x='Space', y='Price')
st.pyplot(fig2)
f"""Pearson correlation beetwen space and price is equal to {round(sp.stats.pearsonr(sample.Price, sample.Space)[0],3)}."""


#Elevator and Price
"""#### Elevator and Price realtionship"""
fig1= plt.figure(figsize=(19,10))
fig1.suptitle('Boxplots of elevator by Price', fontsize=25)
plt.xlabel('elevator', fontsize=25);
plt.ylabel('Price', fontsize=25);
sns.boxplot(data=sample, x='elevator', y='Price')
st.pyplot(fig1)
st.table(data.groupby('elevator')['Price'].agg([np.mean,np.std,np.median]))
f"""Altough the correlation exist bettwen this two variables, ANOVA test is statisticlly insignificant with p-value equal to 
{round(pg.anova(data= sample , dv = 'elevator', between='Rooms')['p-unc'].values[0],3)} which is lower than assumed alpha value - 0.05. """



st.header('Analysis in depth of couple districs')
st.write(data.groupby('district')['Price'].agg([np.mean,np.std,np.median]))

#Districts
"""I will examine two districts in detail. I will start with Srodmiescie district. It is the most expensive district in Warsaw. It is also the most popular one. It is located in the center of Warsaw. Then I will examine Rembertów district. It is the cheapest district in Warsaw. It is located in the south of Warsaw. It is also the least popular one. """

#Srodmiescie
'#### Śródmieście'

sro = data.loc[data['district'] == 'Śródmieście']
fig = plt.figure(figsize=(5, 4))
b = sns.boxplot(x = 'district', y = 'Price',data= sro)
b.set_yticks([ 200000 ,600000 ,1000000 ,1400000 ,1700000 ,2000000,2400000,2800000,3200000,4000000 ])
b.set_ylabel('Price in milions PLN')
#b.ticklabel_format(style= 'plain')
b.set(ylim=(100000, 4000000))
st.pyplot(fig)

#Rembertów
'#### Rembertów'

rem = data.loc[data['district'] == 'Rembertów']
fig = plt.figure(figsize=(5, 4))
b = sns.boxplot(x = 'district', y = 'Price',data= rem)
b.set_yticks([ 200000 ,600000 ,1000000 ,1400000])
b.set_ylabel('Price in milions PLN')
#b.ticklabel_format(style= 'plain')
b.set(ylim=(100000, 1400000))
st.pyplot(fig)

#st.write("Warsaw map")
#st.map()



#Model
st.header('Price prediction model based on proviede data')
st1, st2 = st.columns(2)

district = st1.multiselect( label = 'Enter district' , options = data['district'].unique())
level = st2.multiselect( label = 'Enter level', options = data['level'].unique())
max_level = st1.multiselect( label = 'Enter max_level', options = data['max_level'].unique())
market = st2.multiselect( label = 'Enter market', options= data['Market'].unique())
year = st1.multiselect( label = 'Enter year', options= data['Year'].unique())
elevator = st2.multiselect( label = 'Enter elevator', options= data['elevator'].unique())
parking_place = st1.multiselect( label = 'Enter parking_place', options= data['Parking_place'].unique())
balcony = st2.multiselect( label = 'Enter balcony', options= data['balkon'].unique())
ogrodek = st1.multiselect( label = 'Enter ogrodek', options= data['ogródek'].unique())
taras = st2.multiselect( label = 'Enter taras', options= data['taras'].unique())
street = st1.multiselect( label = 'Enter street', options= data['street'].unique())
Rooms = st2.multiselect( label = 'Enter Rooms', options= data['Rooms'].unique())

space = st.number_input( label = 'Enter space')

predict  = st.button('Predict')
if predict:
    filename = 'gbr_model.sav'
    model = pickle.load(open(filename, 'rb'))
    data = pd.DataFrame([space, Rooms,market,year,elevator,parking_place,balcony,taras,ogrodek,district,street, level,max_level], 
                                               columns=['Space', 'Rooms','Market','Year','elevator','Parkingplace','balkon','taras','ogrdek','district','street', 'level','max_level'])
    data = data.rename(columns = lambda x:re.sub('[^A-Za-z0-9_]+', '', x))
    data = pd.get_dummies(data, columns=['Market','street','district'])
    predictions = model.predict(data)
    if predictions[0] > 0:
        st.success(f'Price is {round(predictions[0],2)} milions PLN')
    else:
        st.write('Ups something went wrong')

