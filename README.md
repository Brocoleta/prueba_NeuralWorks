# Prueba NeuralWorks

## Decisiones y Supuestos

- La mayoria de la información acerca de las decisiones tomadas se encuentra en el colab, pero en resumen, asumi que al ser un
  problema donde se busca predecir los vuelos que se atrasaron, lo mas importante son los True Positives, por lo que busque
  maximizar estos y el recall, debido a que si yo digo que el vuelo no se atraso y no es real, no es grave solo hay que esperar, pero
  si digo que el vuelo se atraso y en verdad no esta atrasado, podria perder el vuelo, por lo que lo importante es que esto no pase,
  logre hacer que haya un 81% de True Positives, lo cual es mucho mejor que el 3% inicial.
- Asumi tambien que como es un set imbalanceado, el accuracy de 82% inicial no es real, ya que esto pasa por que la clase 0 representa
  el 82% de los datos, por lo que si tiro todas las predicciones a esa clase tengo un accuracy alto, pero no es representativo, por
  eso mismo ocupe el recall como metrica.
- Como se muestra en la respuesta de la pregunta 3, asumi que el input es un diccionario, el cual es como si fuera una fila del
  dataset inicial. Es decir, no admite multiples inputs.
- Añadi una nueva columna que es la cantidad de vuelos en la hora programada, estos estan precalculados en el archivo json, vuelos_en_hora, mas informacion se encuentra en el colab
- features.json son todas las features que tiene que recibir el clasificador, hice esto para tenerlas precalculadas, y no tener que
  ir a buscarlas al dataset

## Pregunta 1

Nose si se referian a los modelos iniciales o al GV Grid del XGBoost y Upsampling, si se referian a lo primero, me sale que los
dos modelos tienen las mismas metricas, pero se que XGBoost al ser de tipo arbol, se comporta mejor en datasets inbalanceados
que una Regresion Logistica. Por otro lado si se referian a lo segundo, prefiero el modelo de Upsampling, ya que tiene mas True Positives , es decir podemos detectar mas vuelos atrasados realmente

## Pregunta 2

Las respuestas se encuentran en Respuestas_NeuralWorks.ipynb, al final, en la seccion Respuestas.

## Pregunta 3

La api implementada en Flask se encuentra en app.py, asumi que el input es un diccionario json, el cual tiene los
valores del dataframe inicial, es decir las columnas del excel. Tambien que este input es uno solo, no es un array,
es decir por ejemplo {"TIPOVUELO": "I", "AÑO":"2017",...}

## Pregunta 4

Subi la api a Render, el cual tiene su propio proceso de deploy automatico conectado con Github. El motivo de mi
elección es que Render es un servicio cloud gratuito super rapido de usar, por lo que para el motivo de hacer una
prueba cumple con los requisitos. Si tuviera que hacerlo realmente en produccion, utilizaria servicios cloud de primer nivel
como GCP o AWS donde los servidores son mucho mas estables, rapidos y escalables. \*\* Render cada vez que no se utiliza el server
por un tiempo, se demora un poco mas en iniciarse.

## Pregunta 5
