import numpy as np
import pandas as pd
from datetime import datetime
import json


def get_periodo_dia(fecha):
    fecha_time = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').time()
    mañana_min = datetime.strptime("05:00", '%H:%M').time()
    mañana_max = datetime.strptime("11:59", '%H:%M').time()
    tarde_min = datetime.strptime("12:00", '%H:%M').time()
    tarde_max = datetime.strptime("18:59", '%H:%M').time()
    noche_min1 = datetime.strptime("19:00", '%H:%M').time()
    noche_max1 = datetime.strptime("23:59", '%H:%M').time()
    noche_min2 = datetime.strptime("00:00", '%H:%M').time()
    noche_max2 = datetime.strptime("4:59", '%H:%M').time()

    if (fecha_time > mañana_min and fecha_time < mañana_max):
        return 'mañana'
    elif (fecha_time > tarde_min and fecha_time < tarde_max):
        return 'tarde'
    elif ((fecha_time > noche_min1 and fecha_time < noche_max1) or
            (fecha_time > noche_min2 and fecha_time < noche_max2)):
        return 'noche'


def sacar_hora(dt):
    año = dt.year
    mes = dt.month
    dia = dt.day
    hora = dt.strftime("%H")

    return f"{año}-{mes}-{dia}-{hora}"


def preprocessing_dataframe():
    df = pd.read_csv('dataset_SCL.csv')
    df['periodo_dia'] = df['Fecha-I'].apply(get_periodo_dia)
    features = pd.concat([pd.get_dummies(df['periodo_dia'], prefix='periodo_dia'), pd.get_dummies(df['DIANOM'], prefix='DIANOM'), pd.get_dummies(
        df['SIGLADES'], prefix='SIGLADES'), pd.get_dummies(df['OPERA'], prefix='OPERA'), pd.get_dummies(df['TIPOVUELO'], prefix='TIPOVUELO'), pd.get_dummies(df['MES'], prefix='MES')], axis=1)
    columnas = ['horas_contadas'] + features.columns.tolist()
    with open('features.json', 'w', encoding='utf8') as archivo:
        json.dump(columnas, archivo)

    df['Fecha-Datetime'] = df['Fecha-I'].apply(
        lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    df['fecha_hora'] = df['Fecha-Datetime'].apply(sacar_hora)

    def dif_min(data):
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        dif_min = ((fecha_o - fecha_i).total_seconds())/60
        return dif_min

    df['dif_min'] = df.apply(dif_min, axis=1)
    df['atraso_15'] = np.where(df['dif_min'] > 15, 1, 0)
    df['horas_contadas'] = df.groupby(
        'fecha_hora')['atraso_15'].transform(lambda x: sum(x == 1))

    dictionary = df.set_index('fecha_hora')['horas_contadas'].to_dict()

    with open('vuelos_en_hora.json', 'w', encoding='utf8') as archivo:
        json.dump(dictionary, archivo)

    return


#preprocessing_dataframe()
