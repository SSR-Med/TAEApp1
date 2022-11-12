import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

dat = pd.read_csv('datos.csv')


st.title("Findool")
st.subheader("¡Bienvenido!")
st.write("La elección de una institución de educación superior es una de las más importantes que se pueda tomar, es el lugar donde se empieza, afianza o se reconstruye nuestras prioridades y nuestro estilo de vida. Por tal motivo se ofrece esta aplicación con la finalidad de ayudar a esta persona que está en búsqueda de una institución de educación superior y que cumpla con algunos criterios que son indispensables en su elección.")
st.subheader("¿Para quién va dirigida?")
st.write("Esta aplicación está dirigida para bachilleres que deseen continuar sus estudios en instituciones de educación superior de Estados Unidos.")
st.subheader("¿Cómo funciona?")
st.write("Después de esta explicación encontrarás una serie de criterios, los cuales te pediremos que analices y los ajustes de acuerdo a tus intereses y/o necesidades. Estos filtros que abarcan ámbitos como:")
mark = """
* Económico: Costo promedio de la institución. 
* Geográfico: Búsqueda en un estado en particular o en todo el país. 
* Educativo: Puntuación en SAT, Tasa de admisiones, índice en becasPell y préstamos federales.
"""
col1, col2 = st.columns(2)

with col1:
    st.markdown(mark)

with col2:
   st.image("estudiante.png")

st.write("Luego de ajustar los filtros a tus preferencias le das en aplicar y en el recuadro inferior te aparecerá tu recuadro de resultado con 10 recomendaciones de instituciones y sus respectivos atributos.")



# Institución educativa
tipo = ("Privada","Pública")
terminOption = st.selectbox(
    "Elige el tipo de institución", tipo)
# : Costo neto de la institucion
priceSlider = st.slider("Costo máximo de la institución ",
                          min_value=0, max_value=80000, step=1000)

# : Porcentaje préstamos en institucion
loanSlider = st.slider("¿Qué porcentaje de préstamos federales como mínimo te interesa que hayan en la institución?",
                          min_value=0, max_value=100, step=1)

# : Porcentaje Pell en institucion
pellSlider = st.slider("¿Qué porcentaje de becas Pell como mínimo te interesa que hayan en la institución?",
                          min_value=0, max_value=100, step=1)

#Puntaje SAT
sat = st.number_input('Escribe por favor tu puntaje SAT')

#Estados 
state = ('Todos','AL', 'AK', 'AZ', 'NM', 'AR', 'CA', 'MN', 'CO', 'CT', 'NY', 'DE',
       'DC', 'VA', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'TN', 'MI', 'IA',
       'KS', 'MO', 'KY', 'LA', 'ME', 'MD', 'MA', 'MS', 'MT', 'NE', 'NV',
       'NH', 'NJ', 'NC', 'ND', 'OH', 'WV', 'OK', 'OR', 'PA', 'RI', 'SC',
       'SD', 'TX', 'UT', 'VT', 'WA', 'WI', 'WY', 'AS', 'GU', 'MP', 'PR',
       'FM', 'PW', 'VI', 'MH')
stateOptions = st.selectbox(
        "Elige el estado por el que desees filtrar o selecciona la opción: Todos si te es indiferente el estado",state)

orden = ('Puntaje SAT','Costo', 'Tasa de Admisión')
opcion_ordenar = st.selectbox(
        "Elige la variable prioritaria por la cual deseas ver los resultados ",orden)

diccionario_orden = {'Costo':("NPT4_PRIV","NPT4_PUB"),'Puntaje SAT':"SAT_AVG_ALL", 'Tasa de Admisión':"ADM_RATE_ALL"}

def ordenar (df):
    if opcion_ordenar == 'Puntaje SAT':
        final_df = df.nsmallest(10, ['SAT_AVG_ALL'])
        return final_df

        
    elif  opcion_ordenar == 'Tasa de Admisión':
        final_df = df.nlargest(10, 'ADM_RATE_ALL')
        return final_df
        
    elif opcion_ordenar == 'Costo' and terminOption == "Privada":
        final_df = df.nsmallest(10, 'NPT4_PRIV')
        return final_df

        
    else:
        final_df = df.nsmallest(10, 'NPT4_PUB')
        return final_df

        
    
def top ():
    filtrado = dat[(dat["ADM_RATE_ALL"] <= 1)
             & (dat["PCTFLOAN"]>= (loanSlider/100)) 
             & (dat["PCTPELL"]>= (pellSlider/100))
             & (dat["SAT_AVG_ALL"]<=sat)]
    if terminOption == "Privada":
        filtrado2 = filtrado[filtrado["NPT4_PRIV"]<=priceSlider]
    else:
        filtrado2 = filtrado[filtrado["NPT4_PUB"] <= priceSlider]

    if stateOptions !="Todos":
        filtrado3 = filtrado2[filtrado2["STABBR"] == stateOptions]
        return ordenar(filtrado3)

    return ordenar(filtrado2)

if st.button("Buscar instituciones educativas"):    
    seleccionados = top()
    if terminOption == "Privada":
        nombres = ["INSTNM","STABBR","NPT4_PRIV","SAT_AVG_ALL","ADM_RATE_ALL","PCTPELL","PCTFLOAN"]
    else:
        nombres = ["INSTNM","STABBR","NPT4_PUB","SAT_AVG_ALL","ADM_RATE_ALL","PCTPELL","PCTFLOAN"]
    depurados = seleccionados[nombres]
    depurados.columns = ["Nombre de la institución","Estado","Costo promedio","Puntaje SAT promedio","Tasa de admisión","Porcentaje Becas Pell","Porcentaje préstamos federales"]
    depurados.reset_index(drop=True, inplace=True)
    st.dataframe(depurados)
    st.map(seleccionados)

