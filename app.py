
from flask import Flask, request
import pickle
import json
import pandas as pd
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/', methods=['POST'])
def predict():

    with open('features.json', 'r') as archivo:
        features = json.load(archivo)
        input = request.json
        input = pd.concat([pd.get_dummies(input['OPERA'], prefix='OPERA'), pd.get_dummies(
            input['TIPOVUELO'], prefix='TIPOVUELO'), pd.get_dummies(input['MES'], prefix='MES')], axis=1)
        input = pd.DataFrame(input, index=[0])
        input = input.reindex(columns=features, fill_value=0)

        prediction = model.predict(input)

        output = {'atraso_15': int(round(prediction[0], 2))}

        return json.dumps(output)


if __name__ == "__main__":
    app.run(debug=True)
