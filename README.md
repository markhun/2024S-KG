# 2024S-KG - Book Recommendations

## Running the book recommendations web app

### 1. Ensure external dependencies are installed

First make sure that you have Python 3.10 available on your system and the interpreter is available as a `python3.10` executable.
If you use a system which does not install Python 3.10 as `python3.10` refer to the [troubleshooting section](#Troubleshooting).
Furthermore ensure that `cypher-shell` is available on your system.

### 2. Setup a Python virtual environment and install the app

Execute `make dev`. This will setup a Python virtual environment, install all the necessary dependencies into it and install the `book_recommendations` package itself.

### 3. Start and initalize a Neo4j database

In another shell execute `docker compose up`. This will start a Neo4j database server.

Then execute `make import-neo4j-data`. This will first copy all necessary *.csv files into `./neo4j_db/import/`, a directory made available to the previously started Neo4j database server. It will then continue to execute several Cypher queries to import the *.csv files into the database.
This may take several minutes. Afterwards you should see the following output:

```
>>> The database now contains the following numbers of nodes:
label, count(*)
["Book"], 10000
["Genre"], 443
["Tag"], 2081
["User"], 53424
["Bookseries"], 1794
["Author"], 5841
```

### 4. Generate Embeddings

Run the Python notebook `graph-embeddings.ipynb`. You can use the Python environment created in Step 2 to do so.

### 5. Start the `book-recommendations-app` server

You can now start the book recommendations web app itself by simply executing the command `book-recommendations-app`.
This will start a local web server and automatically open [http://localhost:8501](http://localhost:8501) in your browser.

## Troubleshooting

### Python 3.10 is not installed as `python3.10`

The executable has to be available as `python3.10`. If you use a system, which installs `python3.10` under a
different name (e.g. just `python3`) you may edit the `Makefile` to use this executable instead.

```makefile
PYTHON_VERSION_REQ = python3.10  # Also name of the required python executable 
```

to something like  

```makefile
PYTHON_VERSION_REQ = python3  # Also name of the required python executable 
```

Alternativly you may edit the [Makefile](./Makefile) to make its check more lenient. Be aware though that this software depends on Python 3.10.
Simply editing the Makefile to expect another Python version will probably not work!

## `cypher-shell` is not available on my system

You can download `cypher-shell` from https://neo4j.com/deployment-center/?cypher-shell#tools-tab

It is also possible to simpy download a zip archive containing the executable and editing the `Makefile` to use this executable instead.
For example change 

```makefile
CYPHER_SHELL := cypher-shell  # path to cypher-shell executable
```

to something like  

```makefile
CYPHER_SHELL := .bin/cypher-shell-5.23.0/bin/cypher-shell  # path to cypher-shell executable
```
