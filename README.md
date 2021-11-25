- Set up your cluster connection:

1. download the CA certificate to that directory:
    ~~~
    curl --create-dirs -o ~/.postgresql/root.crt -O https://cockroachlabs.cloud/clusters/<cluster-id>/cert
    ~~~

2. Create a new file named .env and update the new file with the connection string provided:
    ~~~
    CONNECTION_STRING = postgresql://<username>:<password>@<serverless-host>:26257/defaultdb?sslmode=verify-full&sslrootcert='$HOME'/.postgresql/root.crt&options=--cluster=<cluster-name>-<tenant-id>
    ~~~

3. To enter SQL shell connected to the cluster:
    ~~~
    cockroach sql --url "<connection-string>"
    ~~~

<br />

- From the command line, execute the following:

1. create and then activate a virtual environment:
    ~~~
    virtualenv env
    ~~~

    ~~~
    source env/bin/activate
    ~~~

2. Install the required modules to the virtual environment:
    ~~~
    pip3 install psycopg2-binary sqlalchemy sqlalchemy-cockroachdb python-decouple
    ~~~
    or
    ~~~
    pip install -r requirements.txt
    ~~~

3. Initialize the database:
    ~~~
    cat dbinit.sql | cockroach sql --url "<connection-string>"
    ~~~

4. Run the code:
    ~~~
    python3 main.py
    ~~~

5. Exit virtual environment:
    ~~~
    deactivate
    ~~~
