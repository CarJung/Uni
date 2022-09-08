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

def rmanova(data, dv = '', within = '', subject = ''):
    pg.rm_anova(data=data, dv=dv, within=within,subject =subject, detailed=True)

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

def barplot(data, dv = '', group = ''):
    fig, ax = plt.subplots(figsize = (8,6))

    sns.barplot(x =group , y=dv , data = data , capsize = 0.2)

    #ax.set_xlabel('Rodzaj motywacji');
    #ax.set_ylabel('Wynik testu');

    ax.grid(which = 'major', axis= 'y', ls = '--')

    ax.grid(which='minor', axis='y', ls='-.')
    return fig

def extract_data(data, selected_columnnames):
    """Extract columns from the uploaded file by columns selected by the user"""
    return data[selected_columnnames]

def post_hoc(data, dv = '', group = '', round = 3):
    """Post hoc test"""
    return pg.pairwise_ttests(data=data, dv=dv,effsize ='cohen' ,between = group,padjust=('sidak')).round(round)


st.title("Statistical Testing App")

data = st.file_uploader("Upload a dataset. Dataset must be in long format.", type="csv")
wide_long = st.radio("Is the dataset wide or long format?", ('Wide', 'Long'))
if data:
    data = pd.read_csv(data)
    if wide_long == 'Wide':
        index = st.multiselect("Select columns with indexes", data.columns)
        selected_columnnames = data.index.unique()
        #values = data.columns.difference(index)
        #selected_columnnames = st.multiselect("Select columns to analyze", values)
    else: 
        selected_columnnames = st.multiselect("Select columns to analyze", data.columns)
    

select_test = st.selectbox("Select a statistical test", ["T-Test", "ANOVA","Repeated Measure Anova" ,'Correlation', 'Bayesian Testing'])


columns = ['None'] + list(data.columns)

if select_test == "t-test":
    ispaired = st.checkbox("Is paired")
    istwosided = st.checkbox("Is two-sided")
    
if select_test == "ANOVA":
    dv = st.selectbox( "Select a dependent variable", columns)
    group = st.selectbox( 'Select a group variable',columns)
    
if select_test == "Repeated Measure Anova":
    dv = st.selectbox( "Select a dependent variable", columns)
    within = st.selectbox( 'Select a within variable',columns)
    subject = st.selectbox( 'Select a between variable',columns)

if select_test == "Correlation":
    type = st.selectbox('Select a correlation type',['pearson', 'spearman', 'kendall'])   
    
if select_test == "Bayesian testing":
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
        result = anova(data, dv, group)
        st.write(result)
        fig = barplot(data, dv, group)
        st.pyplot(fig)
        post = post_hoc(data, dv, group)
        st.write(post)
    
    if select_test == 'Repeated Measure Anova':
        result = rmanova(data, dv, within, subject)
        st.write(result)
        fig = barplot(data, dv, group)
        st.pyplot(fig)
        post = post_hoc(data, dv, group)
        st.write(post)
        
    if select_test == 'Correlation':
        data = extract_data(data, selected_columnnames)
        result = corr(data, type, selected_columnnames)
        st.write(result)
        fig = corr_plot(data, type)
        st.pyplot(fig)
        heat = heat_plot(data,type)
        st.pyplot(heat)

        
    if select_test == 'Bayesian testing':
        pass