import scipy as sp
import numpy as np
import pingouin as pg

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import streamlit as st


def extract_data(data, selected_columnnames):
    """Extract columns from the uploaded file by columns selected by the user"""
    return data[selected_columnnames]


st.title("Statistical Testing App")

data = st.file_uploader("Upload a dataset", type=["csv", "txt"])

upload = st.button("Upload")
if upload:
    selected_columnnames = st.multiselect("Select columns to analyze", data.columns)

    select_test = st.selectbox("Select a statistical test", ["t-test", "ANOVA"])