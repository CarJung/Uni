import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymongo

@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

@st.experimental_memo(ttl=600)
def get_data():
    db = client.mydb
    items = db.mycollection.find()
    items = list(items)  # make hashable for st.experimental_memo
    return items

items = get_data()

client = init_connection()

data = pd.DataFrame(items)
data =data.iloc[:, 1:]
data['district'] =data['district'].str.replace(" ","")
sample = data.sample(n=500, random_state=42)
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

def distribution_plot():
    
    plt.style.use('ggplot')
    fig, ax = plt.subplots(3,figsize=(19,10))
    fig.suptitle('Distribution of columns')
    sns.histplot(sample, x ='Price', discrete=True, ax = ax[0])
    sns.histplot(sample, x ='Space', discrete=True, ax = ax[1])
    sns.histplot(sample, x ='Room', discrete=True, ax = ax[2])
    return st.pyplot(fig)

distribution_plot()


st.header("Factors that mostly influeces price")


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