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
data['Year'] =data['Year'].str.slice(0,-2)
data['Price'] = data['Price'].astype(float)
data['Space'] = data['Space'].astype(float)
sample = data.sample(n=750, random_state=42)

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

st.write('Śródmieście')

sro = data.loc[data['district'] == 'Śródmieście']
fig = plt.figure(figsize=(5, 4))
b = sns.boxplot(x = 'district', y = 'Price',data= sro)
b.set_yticks([ 200000 ,600000 ,1000000 ,1400000 ,1600000 ,2000000,2400000,2800000,3200000,4000000 ])
b.set_ylabel('Price in milions PLN')
#b.ticklabel_format(style= 'plain')
b.set(ylim=(100000, 4000000))
st.pyplot(fig)



st.write("Warsaw map")
st.map()



st.header('Price prediction model based on proviede data')

district = st.text_input( label = 'Enter district')
level = st.text_input( label = 'Enter level')
max_level = st.text_input( label = 'Enter max_level')
market = st.text_input( label = 'Enter market')
year = st.text_input( label = 'Enter year')
elevator = st.text_input( label = 'Enter elevator')
parking_place = st.text_input( label = 'Enter parking_place')
balcony = st.text_input( label = 'Enter balcony')
ogrodek = st.text_input( label = 'Enter ogrodek')
taras = st.text_input( label = 'Enter taras')
street = st.text_input( label = 'Enter street')

space = st.number_input( label = 'Enter space')

filename = 'gbr_model.sav'

@st.cache
loaded_model = pickle.load(open(filename, 'rb'))
predictions = loaded_model.predict(pd.DataFrame([[street,district, level, max_level, market, year, elevator, parking_place, balcony, ogrodek,taras,street]], 
                                               columns=['street','district', 'level', 'max_level', 'market', 'year', 'elevator', 'parking_place', 'balcony', 'ogrodek','taras','street']))
st.success(f'The predicted price of the flat is ${predictions[0]:.2f} PLN')
