#Empresa
To run this project you will need to install mysql and configure based on the ".env" file.

You can use, and i recommend, docker compose to run the "mysql" database.

To use docker compose, you will need to have docker installed (https://www.docker.com/).

To run the docker compose file, you can use the following command:

```
docker compose up
```

The file for the database schema is db/empresa_db.sql.
You can import the schema to your database using the following command:


```
mysql -u root -p empresa < db/empresa_db.sql

or using docker compose with mysql running in a container:

docker exec -i container_name mysql -u root -p empresa < db/empresa_db.sql

```
After that, on terminal you run this command to install the dependencies and run the project:

```
pip install -r requirements.txt

```
then you can run the project using:

```
python main.py
```

Some names are in portuguese because it's a brazilian project, i'm sorry for that.

If you can help me to improve the code, i would be very grateful!