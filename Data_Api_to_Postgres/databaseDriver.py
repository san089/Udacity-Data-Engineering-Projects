import psycopg2
import configparser
from driver import config


class DatabaseDriver:

    def __init__(self):
        self._conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DATABASE'].values()))
        self._cur = self._conn.cursor()

    def execute_query(self, query):
        self._cur.execute(query)