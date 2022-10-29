import requests
import json


def test_get_set_model_uri():
    requests.post('http://localhost:7999/model', json={'production_model_uri': '/artifacts/test_model.pkl'})
    assert requests.get('http://localhost:7999/model').content.decode('utf-8') == '/artifacts/test_model.pkl'


def test_infer(test_model, test_meta):
    requests.post('http://localhost:7999/model', json={'production_model_uri': '/artifacts/test_model.pkl'})
    assert json.loads(requests.post('http://localhost:7999/infer', json={k:1 for k in test_meta['features']}).text)['predictions'] == [0]

