from flask import Flask, request
import pg8000.native
import sklearn
app = Flask(__name__)
import dill
import pandas as pd


@app.route('/infer', methods=["POST"])
def infer():
    con = pg8000.native.Connection(user='postgres', port='5432', host='172.99.42.2')
    result = con.run("SELECT uri from production_models where id = (select max(id) from production_models)")
    con.close()
    with open(result[0][0], 'rb') as f:
        model = dill.load(f)
    X_pred = pd.DataFrame([[request.json[k] for k in request.json]], columns=[k for k in request.json])
    y_pred = model.predict(X_pred)
    return {'predictions': [int(x) for x in y_pred]}


@app.route('/model', methods=["POST", "GET"])
def model():
    con = pg8000.native.Connection(user='postgres', port='5432', host='172.99.42.2')
    if request.method == "POST":
        new_prod_model_uri = request.json['production_model_uri']
        result = con.run("INSERT INTO production_models(uri) VALUES ('{}')".format(new_prod_model_uri))
        con.close()
        return 'success'
    else:
        result = con.run("SELECT uri from production_models where id = (select max(id) from production_models)")
        con.close()
        return result[0][0]
