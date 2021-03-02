import streamlit as st
import numpy as np 
import matplotlib.pyplot as plt 
from pandas import read_csv
import numpy as np
import pandas as pd
pd.set_option("display.max_columns",None)
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from sklearn.metrics import mean_squared_error
from scipy import stats
import os

option = st.sidebar.selectbox('select option',['Casillas por recibir / recibido','Gráfica con estimador e intervalo','Mapa con casillas'])
st.title('Analisis de casillas')

main = pd.read_csv("Dashboard Estadística/Files/Data/ComputoGobernador2015_Casilla (1).csv") # Alexis
file = main
file['VOTOS NULOS'] = pd.to_numeric(file['VOTOS NULOS'], errors='coerce')
file = file.fillna(0)
g = file.head(20)
st.write(g)



