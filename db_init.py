from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('postgresql://postgres@127.0.0.1:5432/postgres')

engine.execute('CREATE TABLE production_models (id SERIAL NOT NULL, uri varchar(300))')


for file in ['ds_clicks', 'ds_leads', 'ds_offers']:
    df = pd.read_parquet('data/{}.parquet.gzip'.format(file))
    df.to_sql(file, engine)


