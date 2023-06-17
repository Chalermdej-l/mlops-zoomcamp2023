
import pickle
import pandas as pd
import argparse
from sklearn.metrics import mean_squared_error




categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def loadmodel():
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv,model

def predict(df,dv,model):
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    return y_pred


if __name__ == '__main__':        
    year = 2022
    month = 2
    parser = argparse.ArgumentParser()
    parser.add_argument('year')
    parser.add_argument('month')

    args = parser.parse_args()
    year = int(args.year)
    month =int(args.month)
    print('Getting the data')
    df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02}.parquet')
    dv,model = loadmodel()
    print('Predicting...')
    y_predict = predict(df,dv,model)
    result = {
        'year':year,
        'month':month,
        'std':y_predict.std(),
        'mean':y_predict.mean(),
        'error':mean_squared_error(df['duration'],y_predict)
    }
    
    print(result)

