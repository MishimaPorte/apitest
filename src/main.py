from sanic import Sanic

from tortoise import Tortoise, run_async
from configparser import ConfigParser

from elasticsearch_dsl import connections

#Getting data from configuration file.

config = ConfigParser()
config.read("../app.conf")
pg_conf = config["POSTGRES"]

#Tortoise orm settings dictionary.

TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{pg_conf['user']}:{pg_conf['password']}@{pg_conf['host']}:{pg_conf['port']}/{pg_conf['db']}"
    },
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        },
    },
}


async def initdb():

    #Postgres initializer.

    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

#Initializing Sanic app and creating elasticsearch connection.
app = Sanic(name="main")
connections.create_connection(hosts = [config["ELASTIC"]["host"], ], alias = "default")

#importing endpoints.
import endpoints
from db_init import init_dbs

if __name__ == "__main__":

    #Running all init functions and running app.

    run_async(initdb())
    run_async(init_dbs())
    app.run(host = "0.0.0.0", port = 8888)
