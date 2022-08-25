import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('data/data_clean_removed.csv')
data =data.iloc[:, 1:]
data['district'] =data['district'].str.replace(" ","")
st.title('Warsaw flats prices in July of 2022')

st.markdown("""Write about:
            - how was dataset aquired
            - co się w nim znajduje
            - co będzie dalej
            """)
st.write(data.head(20))


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