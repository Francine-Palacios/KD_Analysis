import streamlit as st
from io import BytesIO
import pandas as pd

import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd

import matplotlib.pyplot as plt
import scipy.stats
import seaborn as sns

########################################################################
############### Configuracion e informacion ############################
########################################################################


st.set_page_config(page_title='KDA', layout='wide',
                #    initial_sidebar_state=st.session_state.get('sidebar_state', 'collapsed'),
)

st.image("Departamento_de_matematicas (1).png", use_column_width=True )
st.snow()

texto_descripcion = """
Esta aplicion fue generada para un analisis descripitvo
"""


texto_info = """
- Autor: Francine Palacios - Bastian Aceiton
- Ramo: Laboratorio de Modelación
- Institución: Universidad Tecnica Federico Santa Maria
"""




_, exp_col, _ = st.columns([1,3,1])
with exp_col:
    with st.expander("** Información y usos **"):
        st.markdown(texto_descripcion)
        st.info(texto_info)
        


########################################################################
########################################################################
########################################################################


#########################################################################
################## Barra lateral#########################################
#########################################################################


##################### Informacion en la side bar ########################
        
st.sidebar.title(" Analisis descriptivo de Arizona’s Copper Deposit (KD)")
st.sidebar.caption("Universidad Tecnica Federico Santa María")


#########################################################################

################### Subida de archivo de datos###################################
# uploaded_file = st.sidebar.file_uploader("Cargar el archivo de datos")

# if uploaded_file is None:
      # st.warning('Favor subir el archivo de datos')



#########################################################################
#########################################################################
#########################################################################
st.header('Arizona’s Copper Deposit (KD)')

st.subheader('Contexto: MineLib')

st.write("""
En el desarrollo de **soluciones innovadoras** para la **minería a cielo abierto**, es esencial contar con **herramientas** que permitan la **exploración y optimización** de **problemas complejos**. En este contexto, presentamos nuestra investigación apoyada en **MineLib**, una **biblioteca de problemas de minería a cielo abierto**, que ofrece **instancias de prueba públicamente disponibles** para tres tipos clásicos de problemas de minería: el **problema del límite último de la mina** y dos variantes de **problemas de programación de la producción** en minas a cielo abierto.

Esta biblioteca, similar a la **biblioteca de programación entera mixta (MIPLIB)**, fue desarrollada por **Daniel Espinoza, Marcos Goycoolea, Eduardo Moreno y Alexandra Newman**, y se ha convertido en un **recurso fundamental** para **investigadores y profesionales del sector**. La relevancia de **MineLib** radica en su capacidad para proporcionar un **conjunto estandarizado de problemas** que facilitan la **comparación de algoritmos y técnicas de resolución**.
""")


st.subheader('Contexto del set de datos')
st.write("""
Nuestro análisis se centrará en el estudio del **Depósito de Cobre de Arizona (KD)**, una instancia representativa de los desafíos que enfrenta la **minería a cielo abierto**. Los datos de esta instancia, disponibles en **MineLib**, incluyen un modelo de bloque detallado con dimensiones de bloques de **20x20x15 metros**, y una **precedencia calculada con un ángulo de 45 grados utilizando 8 niveles**. Estos datos son cruciales para comprender las **operaciones y la planificación** en el contexto de un depósito de cobre real, proporcionando una base sólida para nuestro **análisis descriptivo** y la posterior **optimización de la producción**.

La información detallada de los bloques incluye **identificación, coordenadas, tonelaje, valor del bloque, destino** (ya sea mineral o desecho), **porcentaje de cobre** y **ganancia por procesamiento**. Este conjunto de datos nos permitirá explorar la **capacidad de procesamiento de 10 millones de toneladas por año** y la **capacidad de minería ilimitada**, reflejando las condiciones reales de una operación minera a gran escala.

Con estos datos, buscamos no solo avanzar en el **conocimiento técnico de la minería a cielo abierto**, sino también contribuir a la **eficiencia y sostenibilidad** de estas prácticas a través de nuestra investigación aplicada.
""")

st.subheader('Descripción detallada del Modelo de Bloques del Depósito de Cobre de Arizona (KD)')
st.markdown("""

El modelo de bloques para el Depósito de Cobre de Arizona (KD) proporciona información detallada sobre cada bloque dentro de la mina. A continuación se presenta una descripción de cada columna del conjunto de datos:

""")


html_table = """
<table>
  <tr>
    <th>Columna</th>
    <th>Descripción</th>
  </tr>
  <tr>
    <td><strong>id</strong></td>
    <td>Identificador único para cada bloque.</td>
  </tr>
  <tr>
    <td><strong>x</strong></td>
    <td>Coordenada X del bloque en el espacio.</td>
  </tr>
  <tr>
    <td><strong>y</strong></td>
    <td>Coordenada Y del bloque en el espacio.</td>
  </tr>
  <tr>
    <td><strong>z</strong></td>
    <td>Coordenada Z del bloque en el espacio, que suele representar la profundidad.</td>
  </tr>
  <tr>
    <td><strong>tonn</strong></td>
    <td>Tonnage, o peso en toneladas del bloque.</td>
  </tr>
  <tr>
    <td><strong>blockvalue</strong></td>
    <td>Valor del bloque, calculado en base a los costos y ganancias.</td>
  </tr>
  <tr>
    <td><strong>destination</strong></td>
    <td>Destino del bloque, mineral (1) o desecho (2).</td>
  </tr>
  <tr>
    <td><strong>CU %</strong></td>
    <td>Porcentaje de cobre en el bloque.</td>
  </tr>
  <tr>
    <td><strong>process_profit</strong></td>
    <td>Ganancia por procesamiento del bloque.</td>
  </tr>
</table>
"""

st.markdown(html_table, unsafe_allow_html=True)


st.subheader('Aclaraciones')
st.markdown("""
#### Dimensiones del Bloque
            
  Cada bloque tiene dimensiones de $20 \\times 20 \\times 15 \\mathrm{~m}$, lo que representa el volumen físico de cada unidad extraída.

#### Precedencia
            
  En el contexto del Depósito de Cobre de Arizona (KD), la precedencia se calcula utilizando un ángulo de 45 grados y 8 niveles. Esto significa que la extracción de un bloque depende de la extracción previa de otros bloques que están directamente encima de él, formando una especie de “escalera” o “rampa” que respeta el ángulo de inclinación establecido. Este ángulo es importante para mantener la estabilidad de las paredes del pozo y prevenir deslizamientos o derrumbes. Por ejemplo, si un bloque está en un nivel inferior, no se puede extraer hasta que se hayan extraído todos los bloques que están en los niveles superiores y que caen dentro del cono de influencia definido por el ángulo de 45 grados. Esto asegura que no se comprometa la integridad estructural de la mina durante la operación.
            

#### Cálculo del Valor del Bloque
- **Costo de Minería**: Se asume un costo de minería de $-0.75$ por tonelada.
- **Valor del Bloque**: Se calcula como $-0.75^*$ tonn + process_profit.
- **Tasa de Descuento**: Se utiliza una tasa de descuento del $0.15$ para calcular el valor presente del bloque.

#### Tipo de Restricciones
- **Capacidad de Procesamiento**: Se establece una capacidad de procesamiento de $10 \\mathrm{M}$ toneladas por año.
- **Capacidad de Minería**: Se asume una capacidad de minería ilimitada.

Estos datos son fundamentales para realizar un análisis descriptivo y para la planificación y optimización de la producción en la mina.
""")
st.info("""
Para mas informacion puede visitar la pagina del conjunto de datos en [MineLib](https://mansci-web.uai.cl/minelib/kd.xhtml)
""")



#########################################################################
#########################################################################
#########################################################################
    
#########################################################################
###################### Cuerpo de la pagina ##############################
#########################################################################

##################################################################################################
############## Tabla con los datos ############################################
##################################################################################################
path=r'..\Datos\kd.blocks.csv'
df_data = pd.read_csv(path, sep=' ', header=None)
column_names = ['id', 'x', 'y', 'z', 'tonn', 'blockvalue', 'destination', 'CU%', 'process_profit']
df_data.columns=column_names
df_data = df_data.drop('id', axis=1)
st.header('Datos')
st.write("Se elimino la columa 'id' ya que no aporta nueva información, solo es el numero de fila.")
st.dataframe(df_data)
##################################################################################################
############## Tabla con alguans estadisticas de utilidad ################################################
##################################################################################################

st.header('Estadisticas de utilidad')
st.table(df_data.describe())

#########################################################################
#########################################################################
#########################################################################

#########################################################################
############## Graficos #################################################
#########################################################################
st.sidebar.subheader("Plot de datos")
st.sidebar.markdown("Para los graficos de histograma, seleccione las columnas de interes")
if st.sidebar.checkbox("Todas las columnas"):
    feature_names = df_data.columns 
    pass
else:
    columnas=st.sidebar.multiselect('Seleccione las columnas que le interesan para los graficos ', df_data.columns)
    feature_names=columnas

Chance= st.sidebar.slider("¿Cuanto considera que se acepta en 'CU%'?", min_value=0.1,max_value=1.0,value=0.5, step=0.1)

############ Grafico de Histograma ############

st.subheader("Histogramas")

import plotly.express as px


for name in feature_names:
    fig = px.histogram(df_data, x=name, marginal="rug", color_discrete_sequence=['indianred'])
    st.plotly_chart(fig, use_container_width=True)


########## Grafico de Histograma, diferenciando entre la variable objetivo #####
st.subheader("Histograma diferenciado la variable objetivo")

df_aux = df_data.copy()

df_aux['Admit CU%'] = df_aux['CU%'].apply(lambda x: f'Chance > {Chance}' if x > Chance else f'Chance <= {Chance}')

# feature_names = ['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR ', 'CGPA', 'Research', 'Chance of Admit ']

for name in feature_names:
    fig = px.histogram(df_aux, x=name, color='Admit CU%', barmode='overlay',
                       color_discrete_map={f'Chance > {Chance}': 'blue', f'Chance <= {Chance}': 'red'})
    st.plotly_chart(fig, use_container_width=True)




######## Boxplot ###########

st.sidebar.markdown("Para los graficos de Boxplot, seleccione las columnas de interes")
if st.sidebar.checkbox("Todas"):
    feature_names = df_data.columns
    pass
else:
    columnas=st.sidebar.multiselect('Seleccione las columnas que le interesan para el boxplot ', df_data.columns)
    feature_names=columnas

import streamlit as st
import plotly.express as px

# feature_names = ['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR ', 'CGPA', 'Research', 'Chance of Admit ']

for name in feature_names:
    fig = px.box(df_data, y=name, color_discrete_sequence=['goldenrod'])
    fig.update_layout(title=name, yaxis_title="Valor")
    st.plotly_chart(fig, use_container_width=True)








# Slider para seleccionar el rango de 'z'
z_min, z_max = st.slider('Selecciona el rango de profundidad (eje z):', 
                         min_value=int(df_data['z'].min()), 
                         max_value=int(df_data['z'].max()), 
                         value=(int(df_data['z'].min()), int(df_data['z'].max())))

# Filtrado de datos basado en el rango de 'z'
df_filtered = df_data[(df_data['z'] >= z_min) & (df_data['z'] <= z_max)]

# Creación de la figura con Plotly
fig = px.scatter_3d(df_filtered, x='x', y='y', z='z',
                     color='CU%',
                     color_continuous_scale='Viridis',  # Escala de colores
                     range_color=[df_filtered['CU%'].min(), df_filtered['CU%'].max()])

# Actualización de los títulos de los ejes
fig.update_layout(scene=dict(
                    xaxis_title='Eje X',
                    yaxis_title='Eje Y',
                    zaxis_title='Eje Z'),
                  coloraxis_colorbar=dict(title='Porcentaje de Cobre (CU%)'))

# Mostrar la figura en Streamlit
st.plotly_chart(fig)