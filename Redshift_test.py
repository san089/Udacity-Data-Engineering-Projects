import  psycopg2
import configparser

# Loading cluster configurations from cluster.config
config = configparser.ConfigParser()
config.read_file(open('cluster.config'))

def test_connection(host):

    dbname = config.get('DWH','DWH_DB')
    port = config.get('DWH','DWH_PORT')
    user = config.get('DWH','DWH_DB_USER')
    password = config.get('DWH','DWH_DB_PASSWORD')

    con=psycopg2.connect(dbname= dbname, host=host, port= port, user= user, password= password)
    cur = con.cursor()

    cur.execute("CREATE TABLE test (id int);")
    cur.execute("INSERT INTO test VALUES (10);")
    print(cur.execute('SELECT * FROM test'))

    con.close()