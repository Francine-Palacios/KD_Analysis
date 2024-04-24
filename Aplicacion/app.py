import streamlit as st
import pandas as pd
from informacion import Info
from Analisis_descriptivo import Analisis_descriptivo
from Grafico_3d import grafico_3d
from pathlib import Path
import base64


########################################################################
############### Configuracion e informacion ############################
########################################################################


st.set_page_config(page_title='KDA', layout='wide',
                #    initial_sidebar_state=st.session_state.get('sidebar_state', 'collapsed'),
)

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

_, _, col3 = st.columns([3,6,3])

with col3:
    st.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=250 height=60>](https://streamlit.io/)'''.format(img_to_bytes(".\Departamento_de_matematicas (1).png")), unsafe_allow_html=True)

_, col2, _ = st.columns([1,6,1])

with col2:
    st.title('Análisis descriptivo de Arizona’s Copper Deposit (KD)')

texto_descripcion = """
Esta aplicion fue generada para un analisis descripitvo
"""


texto_info = """
- Autor: Francine Palacios - Bastian Aceiton
- Ramo: Laboratorio de Modelación
- Institución: Universidad Tecnica Federico Santa Maria
"""
st.snow()



_, exp_col, _ = st.columns([1,3,1])
with exp_col:
    with st.expander(" Información y usos "):
        st.markdown(texto_descripcion)
        st.info(texto_info)
        


InfoTab,Analisis,Grafico = st.tabs(["Información","Analisis Descriptivo", 'Grafico'])

        
st.sidebar.title("Analisis descriptivo de Arizona’s Copper Deposit (KD) ")
st.sidebar.caption("Universidad Tecnica Federico Santa María")


##################################################################################################
############## Tabla con los datos ############################################
##################################################################################################
path=r'..\Datos\kd.blocks.csv'
df_data = pd.read_csv(path, sep=' ', header=None)
column_names = ['id', 'x', 'y', 'z', 'tonn', 'blockvalue', 'destination', 'CU%', 'process_profit']
df_data.columns=column_names
df_data = df_data.drop('id', axis=1)


with InfoTab:
    Info()

with Analisis:
    Analisis_descriptivo(df_data)

with Grafico:
    grafico_3d(df_data)