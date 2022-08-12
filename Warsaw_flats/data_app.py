import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

data = pd.read_csv('data/data_clean_removed.csv')
data =data.iloc[:, 1:]
st.title('Warsaw flats prices in July of 2022')

st.write("")
st.write(data.head(20))


st.write("Flats by district")

st.write('Śródmieście')
box_plot = px.box(data, y="Price")
st.plotly_chart(box_plot)

st.write("Warsaw map")
st.map()