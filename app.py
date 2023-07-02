
from flask import Flask, request
import pickle
import json
import pandas as pd
from preprocessing import get_periodo_dia, sacar_hora
from datetime import datetime

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
pca = pickle.load(open('pca.pkl', 'rb'))


@app.route('/', methods=['POST'])
def predict():

    with open('features.json', 'r') as archivo:
        with open('vuelos_en_hora.json', 'r') as vuelos_en_hora:

            features = json.load(archivo)
            vuelos_en_hora = json.load(vuelos_en_hora)
            
            input = request.json

            input['periodo_dia'] = get_periodo_dia(input['Fecha-I'])
            input['fecha_hora'] = sacar_hora(
                datetime.strptime(input['Fecha-I'], '%Y-%m-%d %H:%M:%S'))
            try:
                input['horas_contadas'] = vuelos_en_hora[input['fecha_hora']]
            except Exception as e:
                input['horas_contadas'] = 0
            input['horas_contadas'] = pd.DataFrame(
                {'horas_contadas': input['horas_contadas']}, index=[0])
            input = pd.concat([input['horas_contadas'], pd.get_dummies(input['periodo_dia'], prefix='periodo_dia'), pd.get_dummies(input['DIANOM'], prefix='DIANOM'), pd.get_dummies(
                input['SIGLADES'], prefix='SIGLADES'), pd.get_dummies(input['OPERA'], prefix='OPERA'), pd.get_dummies(input['TIPOVUELO'], prefix='TIPOVUELO'), pd.get_dummies(input['MES'], prefix='MES')], axis=1)

            input = pd.DataFrame(input, index=[0])
            input = input.reindex(columns=features, fill_value=0)

            x_test = pca.transform(input)
            prediction = model.predict(x_test)

            output = {'atraso_15': int(round(prediction[0], 2))}

            return json.dumps(output)


if __name__ == "__main__":
    app.run(debug=True)
