import scipy as sp
import numpy as np
import pingouin as pg

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import streamlit as st


def ttest(data,ispaired = False ,isonesided = False ): 
    return pg.ttest(data['A'], data['B'], paired=ispaired, alternative='greater' if isonesided else 'two-sided')

def plot_distri(data):
    fig = plt.figure(figsize=(5, 4))
    sns.distplot(data['A'], label='A')
    sns.distplot(data['B'], label='B')
    plt.xlabel('value')
    plt.ylabel('Density')
    plt.legend()
    return fig

def extract_data(data, selected_columnnames):
    """Extract columns from the uploaded file by columns selected by the user"""
    return data[selected_columnnames]


st.title("Statistical Testing App")

data = st.file_uploader("Upload a dataset", type="csv")
if data:
    data = pd.read_csv(data)
    selected_columnnames = st.multiselect("Select columns to analyze", data.columns)


select_test = st.selectbox("Select a statistical test", ["t-test", "ANOVA"])


if select_test == "t-test":
    ispaired = st.checkbox("Is paired")
    istwosided = st.checkbox("Is two-sided")
    
    

run = st.button("Run Test")
if run:
    if select_test == "t-test":
        data = extract_data(data, selected_columnnames)            
        result = ttest(data, ispaired, istwosided)
        st.write(result)
        fig = plot_distri(data)
        st.pyplot(fig)