from flask import Flask, request, jsonify
from sklearn.externals import joblib
import numpy as np

app = Flask(__name__)

clf = None

def getParameters():
    age = request.args.get('age')
    sex = request.args.get('sex')
    cigsPerDay = request.args.get('cigs')
    totChol = request.args.get('chol')
    sysBP = request.args.get('sBP')
    diabetes = request.args.get('dia')
    diaBP = request.args.get('dBP')
    glucose = request.args.get('gluc')
    heartRate = request.args.get('hRate')

    params = {
        'age': age,
        'sex': sex,
        'cigsPerDay': cigsPerDay,
        'totChol': totChol,
        'sysBP': sysBP,
        'diabetes': diabetes,
        'diaBP': diaBP,
        'glucose': glucose,
        'heartRate': heartRate
    }
    return (params)

@app.route('/predict', methods=['GET'])
def predict():
    params = getParameters()
    input = np.array(
        [[
        int(params['age']),
        int(params['sex']),
        int(params['cigsPerDay']),
        float(params['totChol']),
        float(params['sysBP']),
        float(params['diabetes']),
        float(params['diaBP']),
        float(params['glucose']),
        float(params['heartRate'])
    ]]
    )
    prediction = (clf.predict(input)).tolist()
    probability = (clf.predict_proba(input)).tolist()
    return jsonify(
        {
            'probability': probability,
            'prediction': prediction,
            'data': params
        }
    )

@app.route('/model')
def model():
    coefficients = clf.coef_.tolist()
    intercept = clf.intercept_.tolist()
    return jsonify(
        {
            'model': 'Logistic Regression',
            'coefficients': coefficients,
            'intercept': intercept
        }
    )

if __name__ == '__main__':
    global clf
    clf = joblib.load('./model/logreg.pkl')
    app.run()
