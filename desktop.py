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

import fiona
fiona.drvsupport.supported_drivers['libkml'] = 'rw'
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'
gdl = gpd.read_file("Dashboard Estadística/Files/Poly/DISTRITOS_SONORA.kml")
gdl = gdl[["Name", "geometry"]]
gdl = gdl.sort_values("Name").reset_index(drop=True)
gdl["Porcentaje"] = 0.0

fig, ax = plt.subplots(1, 1,figsize=(20,12))

divider = make_axes_locatable(ax)

#cax = divider.append_axes("right", size="5%", pad=0.1)

gdl.plot(figsize=(20, 20),
         edgecolor = "black",
         column="Porcentaje",
         ax=ax,
         legend=True,
         cmap="Spectral",
         vmax=100,
         vmin=0,
         legend_kwds={'label': "Porcentaje",
                      'orientation': "vertical"})
st.pyplot()


