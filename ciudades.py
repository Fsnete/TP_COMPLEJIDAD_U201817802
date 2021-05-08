from typing import Optional, Hashable

import pandas as pd
import numpy as np
import networkx as nx
import math
from GraphStuff import nx2gv
from BFS import bfs


# Funcion Haversine para hallar la distancia entre dos puntos geograficos
def haversine(cp1, cp2):
    la1, lo1 = float(cp1['LATITUD']), float(cp1['LONGITUD'])
    la2, lo2 = float(cp2['LATITUD']), float(cp2['LONGITUD'])

    lo1, la1, lo2, la2 = map(math.radians, [lo1, la1, lo2, la2])
    dlo = lo2 - lo1
    dla = la2 - la1
    a = math.sin(dla / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dlo / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371

    return round(c * r, 2)


url = "https://raw.githubusercontent.com/lmcanavals/"
url += "algorithmic_complexity/main/data/poblaciones.csv"
poblacionesDF = pd.read_csv(url)

# SACAR LAS PROVINCIAS UNICAS
nomprovincias = poblacionesDF['PROVINCIA'].unique()
provincias = dict()
for nom in nomprovincias:
    provincias[nom] = poblacionesDF[poblacionesDF['PROVINCIA'] == nom]

# ELEGIR Y LISTAS PROVINCIAS
nom_distrito = input("Elige una provincia:")
nomdistritos = provincias[nom_distrito]['DISTRITO'].unique()
print(nomdistritos)
distritos = dict()
provincia = provincias[nom_distrito]
for nom in nomdistritos:
    distritos[nom] = provincia[provincia['DISTRITO'] == nom]

# ELEGIR UN DISTRITO DE LA PROVINCIA ELEGIDA PARA SACAR EL TSP
distrito_elegido = input("Elija un distrito:")
distrito = distritos[distrito_elegido]

# SACA EL GRAFO DE TODOS LOS CENTROS POBLADOS UNIDOS SIN TSP
G = nx.Graph()
col = 'CENTRO POBLADO'

centros_pob = []
for i, cp1 in distrito.iterrows():
    centros_pob.append(cp1[col])

dist = []
print(centros_pob)
for i, cp1 in distrito.iterrows():
    for j, cp2 in distrito.iterrows():
        if cp1[col] != cp2[col]:
            dist.append([cp1[col], haversine(cp1, cp2), cp2[col], 'unconnected'])

tsp_list = []

origen = centros_pob[0]
destino = centros_pob[-1]


for i in range(0, len(dist)-1):
    for j in range(1, len(dist)):
        if dist[i][3] != 'connected' and dist[j][3] != 'connected'\
                and dist[i][0] != origen and dist[j][0] != destino:
            if dist[i][1] <= dist[j][1]:
                tsp_list.append(dist[i])
                dist[i][3] = 'connected'

            elif dist[i][1] >= dist[j][1]:
                tsp_list.append(dist[j])
                dist[j][3] = 'connected'


for element in tsp_list:
    print(element)