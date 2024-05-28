import json
import requests  
import streamlit as st 
from streamlit_lottie import st_lottie 
import pandas as pd


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()    
    
lottie_hello = load_lottieurl('https://lottie.host/e4c4b748-9566-492d-8e07-365b40537b31/aJ1RFaAIYi.json')
lottie_attention = load_lottieurl('https://lottie.host/cf627214-5818-43f0-8ae7-ce5398d16d68/FLoFZxCeba.json')
col1, col2 = st.columns([1, 3])

with col1:
    st_lottie(
        lottie_hello,
        speed= 1,
        reverse= False,
        loop= True,
        quality= 'hight',
        height= None,
        width= None,
        key= None
    )

with col2:
    st.title('Codificación para Suelos')

    st.write("""
    ##### Tabla 1 - Tipos de suelos junto con sus códigos correspondientes.
    """)

    datos_suelos = {
        'Tipo de Suelo': ['Arena', 'Arena Limosa', 'Arena limo-arcillosa', 'Arena arcillosa', 'Arena arcillosa-limosa',
                            'Limo', 'Limo Arenoso', 'Limo areno-arcilloso', 'Limo arcilloso', 'Limo arcilloso-arenoso',
                            'Arcilla', 'Arcilla arenosa', 'Arcilla arenosa-limosa', 'Arcilla limosa', 'Arcilla limosa-arenosa'],
        'Código': [1, 12, 123, 13, 132, 2, 21, 213, 23, 231, 3, 31, 312, 32, 321]
    }

    df = pd.DataFrame(datos_suelos)
    st.dataframe(df, width=500, height=560, hide_index=True)

    datos_pilotes = {
    'Tipo de Pilote': ['Excavada', 'Raíz', 'Hélice contínua'],
    'Denominación': ['Excavada', 'Raíz', 'HCM'],
    }

    st.write("""
    ##### Tabla 2 - Tipos de pilotes.
    """)

    df = pd.DataFrame(datos_pilotes)
    st.dataframe(df, hide_index=True)

st.write("""
##### Configuración de los datos en Excel
En este video, se muestra cómo configurar adecuadamente los datos de tipo de suelo y NSPT en el archivo de Excel. Siga las instrucciones detalladas para asegurar que los datos se ingresen correctamente.
""")

video_file = open('./Video/Excel.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)

