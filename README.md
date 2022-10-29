# click classification demo

###Overview:
1. Architecture choices - I would normally implement a system such as this using Kubeflow, Google Cloud Storage, Vertex AI and Google Cloud SQL. The requirements called for local testing, however and mocking these services locally would take more time than is scoped. Therefore, I've used Docker, running Postgres, Flask/Gunicorn and custom pipeline and artifact logic.
2. Use - In order to run the two pipelines (one with regularization and one without), run `./spin_up.sh`. The resulting artifacts will be persisted to the `artifacts` directory. 

###Granular Requirements:

####1: Creating a Feature Database
We’d like to spin up a relational database that can store our data for training models. For this task, please perform the following:

Write code (Dockerfile/docker-compose, a shell script, etc) that spins up a relational database we can use to store our feature data.  Please use an open source RDBMS such as SQLite.
    
**Postgres database is spun up via docker and added to the docker network. Security is disabled as this is a minimal example and very limited from a time perspective.**

For each of the tables provided, write SQL DDL that defines a table schema for the data to be stored in the database.
    
**Tables are created via `pandas`' and `sqlalchemy`'s `to_sql` functonality.**

Write code that can load the parquet file into its respective table in the database.
    
**Tables are filled with the same functionality as they are created.**

Create the tables in the database using the DDL from step 1.
    
**The feature tables are created via via `pandas`' and `sqlalchemy`'s `to_sql` functonality, however an additional table tracking production model URIs is created via `CREATE TABLE`.**

Perform a load of the datasets into the tables, using the code you wrote in step 3.
    
**Features are loaded and joined in the `_ingest` function within `ml/run_pipeline.py`**

####2: Model Training Functionality
Now that we have our feature data in a database, we can write code that can produce a model artifact that can be consumed by a model service. Please do the following:
Write code that can read the data from the database into memory, as a data frame or similar tabular data structure suitable for model training.
    
**Features are loaded and joined in the `_ingest` function within `ml/run_pipeline.py`**

Write code that, given the set of tables fetched from the previous step, will preprocess the data into a single, model ready dataset. This can include joins, one-hot encoding, etc.
    
**Features are loaded and joined in the `_ingest` function within `ml/run_pipeline.py`**

NOTE: as stated before, do not spend time on exploratory analysis; it is not needed.
Write code that can train a logistic regression model on a feature dataset (dataframe or otherwise) and also export this model in some consumable format.
This will take, as input, the dataset created from step 2.
Your target variable is a binary label of whether or not an offer is clicked.
This function(s) should allow you to specify hyper parameters as input.
You should include functionality for exporting the model as an artifact that can be consumed by the model server.  This can be a serialized object (pickle file), a configuration file (list of coefficients), or other portable format.
    
**Model is trained in the `_train` function within `ml/run_pipeline.py`**

Remember that, as with data exploration, we do NOT grade on model quality at all, simply that you can create a model artifact.
Using the code designed in the previous step to build two logistic regression models with two different hyper parameter sets (the specifics don’t matter here). This should yield you two different model artifacts.
    
**A second function call to `run_pipeline` is made at the end of `ml/run_pipeline.py`, setting regularization to none as opposed to the default l2.**

Again, we do NOT grade on quality, simply on having a set of models.
####3: Build the Model Server
The final piece is the model server. It is a web app that produces model predictions upon receiving a POST request.  It should also easily allow model swapping. 

We need you to:
Write a simple web application that has three endpoints that do the following:

Single Model Prediction: An endpoint that accepts a POST request with a JSON body of feature data for an offer shown to a lead, and returns the probability of click occurring.

Model Assignment: An endpoint that accepts a POST request with a JSON body specifying a particular model to use for “production” inference. The nature of the body doesn’t matter so long as the app can load the new model you specify (again, pickle file, zip binary, coefficients, etc).

Model Verification: An endpoint that accepts a GET request that returns an identifier of the current model used “in production”, i.e. in this app.
    
**The server is written in `server/main.py`.**

Yes, this does require having a concept of a “model id” in the app, but we’ll let you decide how to handle that.

**The server uses the `production_model` table in the postgres database to track production model URIs.**

Write a simple python script that generates feature data and produces POST/GET requests to test all three endpoints from your web application. Record the requests/responses as part of your submission (a text file or code comment, etc).
    
**The routes are tested in `test/test_routes.py` via `pytest`**
    