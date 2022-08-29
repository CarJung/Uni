import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from google.oauth2 import service_account
from gsheetsdb import connect
import scipy as sp
import pingouin as pg

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

#data proccesing
data = pd.DataFrame(rows)
data['district'] =data['district'].str.replace(" ","")
data['Year'] = data['Year'].astype(str) 
data['Year'] =data['Year'].str.slice(0,-2)
sample = data.sample(n=750, random_state=42)

st.title('Warsaw flats prices in July of 2022')
st.markdown("""This is a small data science report about real estate market in Warsaw. This dataset was made purely my me. I have scrapped flats offers from Otodomo page.
            Dataset consist of 15 columns.\\
            Thing you can find in the report: \\
            - Dataset reiview \\
            - Factors that mostly influece price \\
            - Analysis in depth of couple districs \\
            - Model predicting price of a flat based on provided features
            
""")


st.header("Dataset reiview")
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

f"""ANCOVA realtionship beetwen rooms and price{pg.anova(data= sample , dv = 'Price', between='Rooms')} """
fig1= plt.figure(figsize=(19,10))
fig1.suptitle('Distribution of rooms column', fontsize=25)
sns.boxplot(data=sample, x='Rooms', y='Price')
st.pyplot(fig1)

f"""Pearson correlation beetwen space and price{sp.stats.pearsonr(sample.Price, sample.Space)} """
fig2= plt.figure(figsize=(19,10))
fig2.suptitle('Distribution of rooms column', fontsize=25)
sns.scatterplot(data=sample, x='Space', y='Price')
st.pyplot(fig2)

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