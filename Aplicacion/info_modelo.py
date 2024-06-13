import streamlit as st

def contenido_info_modelo():
    contenido_html = """
    <h1>Resumen y Consideraciones del Proyecto </h1>

    <h2>Transformación de Datos</h2>

    <p>Utilizamos la transformación de Box-Cox para normalizar la distribución de nuestros datos, lo cual es crucial para mejorar la precisión de los modelos geoestadísticos. La transformación de Box-Cox requiere que los datos sean estrictamente positivos. Dado que nuestros datos a predecir son porcentajes, no hay problema con la no negatividad. Sin embargo, muchos de los porcentajes son 0, por lo que transformamos la variable "porcentaje de cobre" a "no porcentaje de cobre" restando el valor del dato a 100 (es decir, su complemento), para cumplir con la hipótesis de positividad. Además, dividimos por 100 para ajustar la escala.</p>

    <p>La elección del parámetro lambda  de la transformación Box-Cox se realizó mediante la técnica del "codo", que busca el valor de \(\lambda\) que maximiza la verosimilitud logarítmica. Utilizamos la librería MASS de R para calcular automáticamente el lambda óptimo, que resultó ser aproximadamente 145.</p>

    <h2>Análisis de Variograma</h2>

    <p>Asumimos tanto una media constante en los datos como una media variable. Calculamos dos variogramas empíricos y seleccionamos el de Cressie y Hawkins por ser más robusto frente a valores atípicos.</p>

    <table style="width:50%; margin-left:auto; margin-right:auto;">
    <tr>
        <th>Modelo</th>
        <th>SSE</th>
    </tr>
    <tr>
        <td>Esférico</td>
        <td>3.95533 &times; 10<sup>-8</sup></td>
    </tr>
    <tr>
        <td>Exponencial</td>
        <td>8.264444 &times; 10<sup>-8</sup></td>
    </tr>
    <tr>
        <td>Gaussiano</td>
        <td>3.984313 &times; 10<sup>-8</sup></td>
    </tr>
    <tr>
        <td>Lineal</td>
        <td>3.911204 &times; 10<sup>-8</sup></td>
    </tr>
    </table>

    <h2>Kriging Simple</h2>

    <p>Para el kriging simple, calculamos la media conocida como el promedio general de la variable a predecir.</p>

    <pre>
    Root Mean Squared Error (RMSE): 0.0006955978 
    Mean Absolute Error (MAE): 0.0003329818
    </pre>

    <h2>Kriging Ordinario</h2>

    <p>En el kriging ordinario, no asumimos que conocemos la media, sino que la estimamos. Los resultados fueron muy similares:</p>

    <pre>
    Root Mean Squared Error (RMSE): 0.0006966028 
    Mean Absolute Error (MAE): 0.0003321576
    </pre>

    <h2>Kriging Universal</h2>

    <p>Finalmente, intentamos un kriging universal, ya que detectamos cierta tendencia en algunas direcciones. Esto se observó utilizando regresiones lineales en cada coordenada. Los resultados indicaron una tendencia significativa, lo que sugiere que la suposición de media constante en los modelos de kriging anteriores es cuestionable.</p>

    <h3>Regresión respecto a la coordenada x</h3>

    <table style="width:50%; margin-left:auto; margin-right:auto;">
    <tr>
        <th></th>
        <th>Estimate</th>
        <th>Std. Error</th>
        <th>t value</th>
        <th>Pr(&gt;|t|)</th>
    </tr>
    <tr>
        <td>(Intercept)</td>
        <td>-4.641e-03</td>
        <td>4.326e-05</td>
        <td>-107.3</td>
        <td>&lt;2e-16 ***</td>
    </tr>
    <tr>
        <td>a$x</td>
        <td>6.308e-05</td>
        <td>9.487e-07</td>
        <td>66.5</td>
        <td>&lt;2e-16 ***</td>
    </tr>
    </table>

    <h3>Regresión respecto a la coordenada y</h3>

    <table style="width:50%; margin-left:auto; margin-right:auto;">
    <tr>
        <th></th>
        <th>Estimate</th>
        <th>Std. Error</th>
        <th>t value</th>
        <th>Pr(&gt;|t|)</th>
    </tr>
    <tr>
        <td>(Intercept)</td>
        <td>-4.310e-03</td>
        <td>5.114e-05</td>
        <td>-84.28</td>
        <td>&lt;2e-16 ***</td>
    </tr>
    <tr>
        <td>a$y</td>
        <td>1.208e-04</td>
        <td>2.504e-06</td>
        <td>48.26</td>
        <td>&lt;2e-16 ***</td>
    </tr>
    </table>
    <h3>Regresión respecto a la coordenada z</h3>

    <table style="width:50%; margin-left:auto; margin-right:auto;">
    <tr>
        <th></th>
        <th>Estimate</th>
        <th>Std. Error</th>
        <th>t value</th>
        <th>Pr(&gt;|t|)</th>
    </tr>
    <tr>
        <td>(Intercept)</td>
        <td>-4.427e-03</td>
        <td>6.255e-05</td>
        <td>-70.77</td>
        <td>&lt;2e-16 ***</td>
    </tr>
    <tr>
        <td>a$z</td>
        <td>2.264e-04</td>
        <td>5.586e-06</td>
        <td>40.53</td>
        <td>&lt;2e-16 ***</td>
    </tr>
    </table>
    <h3>Cálculo del Variograma Empírico/Teórico</h3>

    <p>Volvimos a calcular el variograma empírico/teórico asumiendo la tendencia. Utilizamos los mismos modelos y obtuvimos los siguientes resultados:</p>

    <table style="width:50%; margin-left:auto; margin-right:auto;">
    <tr>
        <th>Modelo</th>
        <th>SSE</th>
    </tr>
    <tr>
        <td>Esférico</td>
        <td>2.235154 &times; 10<sup>-8</sup></td>
    </tr>
    <tr>
        <td>Exponencial</td>
        <td>4.414818 &times; 10<sup>-8</sup></td>
    </tr>
    <tr>
        <td>Gaussiano</td>
        <td>9.676946 &times; 10<sup>-9</sup></td>
    </tr>
    <tr>
        <td>Lineal</td>
        <td>1.75465 &times; 10<sup>-8</sup></td>
    </tr>
    </table>
    
    <p> Los resultados de las predicciones usando K-Folds, con 10 folds al igual que antes fue de : 
      <pre>
    Root Mean Squared Error (RMSE): 0.0006768341 
    Mean Absolute Error (MAE): 0.0002693542 
    </pre>
    
    <h2>Resumen de Métricas para Kriging</h1>

    <table style="width:70%; margin-left:auto; margin-right:auto; border: 1px solid black; border-collapse: collapse;">
    <tr>
        <th>Modelo</th>
        <th>Root Mean Squared Error (RMSE)</th>
        <th>Mean Absolute Error (MAE)</th>
    </tr>
    <tr>
        <td>Kriging Simple</td>
        <td>0.0006955978</td>
        <td>0.0003329818</td>
    </tr>
    <tr>
        <td>Kriging Ordinario</td>
        <td>0.0006966028</td>
        <td>0.0003321576</td>
    </tr>
    <tr>
        <td>Kriging Universal</td>
        <td>0.0006768341</td>
        <td>0.0002693542</td>
    </tr>
    </table>
    <h2>Diferencia entre RMSE y MAE</h2>

    <p>El Root Mean Squared Error (RMSE) y el Mean Absolute Error (MAE) son dos métricas comunes para evaluar la precisión de los modelos de predicción.</p>

    <ul>
        <li><strong>RMSE:</strong> Es sensible a los errores grandes debido a la operación de elevación al cuadrado.</li>
        <li><strong>MAE:</strong> Proporciona una medida lineal de los errores, sin dar un peso adicional a los errores más grandes.</li>
    </ul>

    <p>En nuestro análisis, el RMSE para kriging universal se mantuvo casi igual que para los métodos simples y ordinarios, indicando que los errores grandes son similares entre estos métodos. Sin embargo, el MAE disminuyó considerablemente en el kriging universal, sugiriendo una mejora en la precisión general del modelo.</p>

    <h2>Conclusiones</h2>

    <p>En este estudio, aplicamos diferentes técnicas de kriging para predecir el porcentaje de cobre en una muestra de datos. Los métodos empleados incluyen kriging simple, kriging ordinario y kriging universal.</p>

    <ul>
        <li><strong>Kriging Simple:</strong> Este método asume una media constante conocida, calculada como el promedio general de los datos.</li>
        <li><strong>Kriging Ordinario:</strong> A diferencia del kriging simple, este método no asume que la media es conocida, sino que la estima a partir de los datos.</li>
        <li><strong>Kriging Universal:</strong> Este método permite modelar una tendencia en los datos, lo que lo hace más flexible.</li>
    </ul>

    <p>De los resultados obtenidos, podemos concluir que el kriging universal es el mejor modelo para nuestros datos, ya que presenta los menores valores de RMSE y MAE. Esto sugiere que tener en cuenta la tendencia en los datos mejora la precisión de las predicciones.</p>

    <p>Es importante considerar que esto se debe en parte a que los datos y la transformación aplicada mantienen los valores en una escala reducida. La reducción en el error absoluto sugiere que estamos en el camino correcto para mejorar nuestras predicciones.</p>
    <h2>Comparación de las Predicciones entre Métodos</h2>

    <p>Se predijo desde el valor mínimo hasta el valor máximo de cada coordenada, realizando así la predicción en un cubo que contiene los datos reales.</p>

    <p>A continuación, se presenta una gráfica que muestra las diferencias entre las predicciones utilizando los métodos de kriging simple, ordinario y universal.</p>

    """

    
    st.markdown(contenido_html, unsafe_allow_html=True)
    return None 