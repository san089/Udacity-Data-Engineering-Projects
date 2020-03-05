import psycopg2
import configparser
from pathlib import Path
from queries import create_business_schema, create_business_table

config = configparser.ConfigParser()
config.read_file(open(f"{Path(__file__).parents[0]}/config.cfg"))

class DatabaseDriver:

    def __init__(self):
        self._conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DATABASE'].values()))
        self._cur = self._conn.cursor()

    def execute_query(self, query):
        self._cur.execute(query)

    def setup(self):
        self.execute_query(create_business_schema)
        self.execute_query(create_business_table)