from sqlalchemy import create_engine
import pandas as pd
from sklearn.linear_model import LogisticRegression
import dill
import json
import os


def _ingest(df_uri):
    engine = create_engine('postgresql+pg8000://postgres@{}:5432/postgres'.format('172.99.42.2'))
    df_clicks = pd.read_sql_query('select * from ds_clicks', con=engine).set_index('index')
    df_leads = pd.read_sql_query('select * from ds_leads', con=engine).set_index('index')
    df_offers = pd.read_sql_query('select * from ds_offers', con=engine).set_index('index')
    df = df_offers.merge(df_clicks, on='offer_id', how='left').merge(df_leads, on='lead_uuid', how='left')
    df['clicked'] = df['clicked_at'].isnull()
    df.to_parquet(df_uri)
    return df


def _train(input_params: dict, df_train_uri: str, model_uri, meta_uri):

    df = pd.read_parquet(df_train_uri)

    model = LogisticRegression(**input_params)
    df = pd.get_dummies(df, columns=['loan_purpose', 'credit'])
    df['requested'] = df['requested'].fillna(0)
    df['annual_income'] = df['annual_income'].fillna(0)
    df = df[df['apr'].notna()]
    meta = {'params':{p:getattr(model, p)for p in model.get_params()}, 'features': [c for c in df.columns if not c in ['lead_uuid', 'offer_id', 'clicked_at', 'clicked']]}
    model.fit(df[meta['features']], df['clicked'])
    with open(model_uri, 'wb') as f:
        dill.dump(model, f)
    with open(meta_uri, 'w') as f:
        json.dump(meta, f)
    return model, meta


def pipeline(input_params: dict, df_uri: str, model_uri: str, meta_uri: str):
    _ingest(df_uri=df_uri)
    _train(input_params=input_params, df_train_uri=df_uri, model_uri=model_uri, meta_uri=meta_uri)


def run_pricing_pipeline(pipeline_root, input_params):
    if not os.path.isdir(pipeline_root):
        os.makedirs(pipeline_root)
    df_uri = '{}/df.parquet'.format(pipeline_root)
    model_uri = '{}/model.pkl'.format(pipeline_root)
    meta_uri = '{}/meta.json'.format(pipeline_root)
    pipeline(input_params= input_params, df_uri=df_uri, model_uri=model_uri, meta_uri=meta_uri)


run_pricing_pipeline(input_params={}, pipeline_root='/artifacts/run1')
run_pricing_pipeline(input_params={"penalty": 'none'}, pipeline_root='/artifacts/run2')

