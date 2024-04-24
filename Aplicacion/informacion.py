import streamlit as st




def Info():
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

    return None 