import scipy as sp
import numpy as np
import pingouin as pg

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import streamlit as st


def ttest(data,ispaired = False ,isonesided = False, columns = []): 
    return pg.ttest(data[columns[0]], data[columns[1]], paired=ispaired, alternative='greater' if isonesided else 'two-sided')

def anova(data, dv = '', group = ''):
    return pg.anova(data = data, dv=dv, between=group)

def corr(data, method = 'pearson',columns = []):
    return pg.corr(x=data[columns[0]],y=data[columns[1]], method = type)

def bayes():
    return None

def plot_bidistri(data):
    fig = plt.figure(figsize=(5, 4))
    sns.distplot(data['A'], label='A')
    sns.distplot(data['B'], label='B')
    plt.xlabel('value')
    plt.ylabel('Density')
    plt.legend()
    return fig

def heat_plot(data, method = 'pearson'):
    fig = plt.figure(figsize=(5, 4))
    sns.heatmap(data.corr(method = method), annot=True)
    return fig

def corr_plot(data, method = 'pearson'):
    fig = plt.figure(figsize=(5, 4))
    sns.scatterplot(data=data, x='A', y='B')
    return fig

def boxplot(data, dv = '', group = ''):
    fig = plt.figure(figsize=(5, 4))
    sns.boxplot(data=data, x=group, y=dv)
    return fig

def extract_data(data, selected_columnnames):
    """Extract columns from the uploaded file by columns selected by the user"""
    return data[selected_columnnames]


st.title("Statistical Testing App")

data = st.file_uploader("Upload a dataset", type="csv")
if data:
    data = pd.read_csv(data)
    selected_columnnames = st.multiselect("Select columns to analyze", data.columns)


select_test = st.selectbox("Select a statistical test", ["t-test", "ANOVA" ,'Correlation', 'Bayesian ANOVA'])


if select_test == "t-test":
    ispaired = st.checkbox("Is paired")
    istwosided = st.checkbox("Is two-sided")
    
if select_test == "ANOVA":
    dv = st.selectbox( "Select a dependent variable", data.columns)
    group = st.selectbox( 'Select a group variable',data.columns)
    
if select_test == "Correlation":
    type = st.selectbox('Select a correlation type',['pearson', 'spearman', 'kendall'])   
    
if select_test == "Bayesian ANOVA":
    likelihoods = st.selectbox('Select likelihoods', ['Student-t', 'Normal', 'Lognormal', 'Poisson', 'Gamma', 'Inverse-Gamma', 'Beta', 'Uniform'])           

run = st.button("Run Test")
if run:
    if select_test == "t-test":
        data = extract_data(data, selected_columnnames)            
        result = ttest(data, ispaired, istwosided, selected_columnnames)
        st.write(result)
        fig = plot_bidistri(data)
        st.pyplot(fig)
        
    if select_test == 'ANOVA':
        data = extract_data(data, selected_columnnames)            
        result = anova(data, dv, group)
        st.write(result)
        fig = boxplot(data, dv, group)
        st.pyplot(fig)
        
    if select_test == 'Correlation':
        data = extract_data(data, selected_columnnames)
        result = corr(data, type, selected_columnnames)
        st.write(result)
        fig = corr_plot(data, type)
        st.pyplot(fig)
        heat = heat_plot(data,type)
        st.pyplot(heat)

    if select_test == 'Bayesian ANOVA':
        pass