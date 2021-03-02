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

file = pd.read_csv("Dashboard Estadística/Files/Data/ComputoGobernador2015_Casilla (1).csv") # Alexis
muestra_actual = pd.read_csv("Dashboard Estadística/Files/Exports/PAQUETES.csv")

st.subheader('Muestra actual')
st.write(muestra_actual)

df_dic = muestra_actual.groupby("DISTRITO.LOCAL").agg({"PAN":"count"}).reset_index().rename(columns={"PAN" : "TOTAL"})

st.write(df_dic)

sim = pd.DataFrame()
# Declara el DataFrame de varianzas
varianzas = pd.DataFrame()
# Crear dataframe muestra
muestra = pd.DataFrame()
# Crear dataframe muestra distritos
muestra_distritos = pd.DataFrame()
for index,row in df_dic.iterrows():
    total_distrito = file[file["DISTRITO LOCAL"] == row[0]].iloc[:,:]
    # obtener muestra por distrito
    muestra_dis = muestra_actual[muestra_actual["DISTRITO.LOCAL"] == row[0]]
    m1 = muestra_dis.iloc[:, 5:]
    cociente = len(total_distrito)/len(m1)
    suma_dis = cociente*(m1.sum())
    # agregamos a nuestros dataframes de la simulacion actual
    muestra_distritos = muestra_distritos.append(suma_dis, ignore_index = True)
    # agregamos la muestra con todos los datos
    muestra = muestra.append(muestra_dis, ignore_index = True)

# calculamos la proporcion de la simulacion
X_gorro = muestra_distritos.sum()["VOTACION.TOTAL.EMITIDA"]
# Una Y__gorro por partido
Y_gorros = muestra_distritos.sum()
suma = Y_gorros / X_gorro
sim = sim.append(suma, ignore_index = True)

# Calculamos la varianza
varianza_distritos = pd.DataFrame()
for index,row in df_dic.iterrows():
    total_distrito = file[file["DISTRITO LOCAL"] == row[0]].iloc[:,:]
    tmp_dis_varianza = muestra[muestra["DISTRITO.LOCAL"] == row[0]].iloc[:,5:]
    Nh = len(total_distrito)
    nh = row[1]

    tmp_var = pd.DataFrame()
    for index, row_var in tmp_dis_varianza.iterrows():
        G_hi = (row_var - (suma * row_var["VOTACION.TOTAL.EMITIDA"])) / X_gorro
        tmp_var = tmp_var.append(G_hi, ignore_index = True)

    # Calculamos las Gh
    G_h = tmp_var.sum()/nh
    # Data frame para guardar la resta al cuadrado de las (Ghi - Gh)^2
    tmp_var_square = pd.DataFrame()
    for index, row_var in tmp_var.iterrows():
        sub_square_tmp = (row_var - G_h) ** 2
        tmp_var_square = tmp_var_square.append(sub_square_tmp, ignore_index = True)

    var_Ghi = tmp_var_square.sum()/(row[1] - 1)
    var_distrito = (Nh ** 2) * ((1/nh) - (1/Nh)) * var_Ghi
    varianza_distritos = varianza_distritos.append(var_distrito, ignore_index = True)

varianzas = varianzas.append(varianza_distritos.sum(), ignore_index = True)

st.subheader('Simulación')
st.write(sim)

st.subheader('Varianzas')
st.write(varianzas)


st.subheader('Delta')
delta = 2.575 * (varianzas ** (1/2))
st.write(delta)

# --- INTERVALOS ---
intervalo_PAN = pd.DataFrame({"estimacion": sim["PAN"][:].array, "delta": delta["PAN"].array})
intervalo_PAN["minimo"] = intervalo_PAN["estimacion"] - intervalo_PAN["delta"]
intervalo_PAN["maximo"] = intervalo_PAN["estimacion"] + intervalo_PAN["delta"]


intervalo_COALICION = pd.DataFrame({"estimacion": sim["COALICION"][:].array, "delta": delta["COALICION"].array})
intervalo_COALICION["minimo"] = intervalo_COALICION["estimacion"] - intervalo_COALICION["delta"]
intervalo_COALICION["maximo"] = intervalo_COALICION["estimacion"] + intervalo_COALICION["delta"]

st.subheader('Intervalo PAN')
st.write(intervalo_PAN)

st.subheader('Intervalo coalición')
st.write(intervalo_COALICION)

dl = pd.read_csv("Dashboard Estadística/Files/Data/Casillas.csv")
#del dl["Unnamed: 4"]
dl.columns = ["NOMBRE", "CODIGO", "CAPTURADAS", "MUESTRA"]
del dl["CAPTURADAS"]
st.subheader('Casillas')
st.write(dl)

contadas = muestra_actual
contadas["CASILLAS"] = 1
contadas = contadas[["DISTRITO.LOCAL", "CASILLAS"]]
contadas = contadas.groupby("DISTRITO.LOCAL").sum()
contadas.reset_index(inplace=True)
contadas.columns = ["NOMBRE","CASILLAS"]
st.subheader('Casillas contadas')
st.write(contadas)

dl = dl.merge(contadas, on="NOMBRE")
#st.write(dl)

dl["PORCENTAJE"] = (dl["CASILLAS"]/dl["MUESTRA"])*100
st.subheader('Porcentaje')
st.write(dl)


st.set_option('deprecation.showPyplotGlobalUse', False)

import fiona
fiona.drvsupport.supported_drivers['libkml'] = 'rw'
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'
gdl = gpd.read_file("Dashboard Estadística/Files/Poly/DISTRITOS_SONORA.kml")
gdl = gdl[["Name", "geometry"]]
gdl = gdl.sort_values("Name").reset_index(drop=True)
gdl["Porcentaje"] = 0.0

for index, row in dl.iterrows():
    gdl.loc[gdl["Name"] == row["CODIGO"], "Porcentaje"] = row["PORCENTAJE"]

fig, ax = plt.subplots(1, 1,figsize=(20,12))

divider = make_axes_locatable(ax)

st.subheader('Representación grafica')

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

y = dl["PORCENTAJE"]

st.subheader('Porcentaje')
figura = dl.plot.bar(figsize=(20,10),
            rot=0,
            x="CODIGO",
            y="PORCENTAJE",
            ylim=(0,100))
st.pyplot()
