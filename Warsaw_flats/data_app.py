import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('data/data_clean_removed.csv')

st.title('Warsaw flats prices in July of 2022')