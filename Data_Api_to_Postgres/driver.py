import configparser
from pathlib import Path
from businesssearch import BusinessSearch
from queries import create_business_schema, create_business_table, insert_business_table
from databaseDriver import DatabaseDriver

config = configparser.ConfigParser()
config.read_file(open(f"{Path(__file__).parents[0]}/config.cfg"))

api_key = config['KEYS']['API_KEY']
headers = {'Authorization': 'Bearer %s' % api_key}

def to_string(data):
    return [str(value) for value in data.values()]

def main():

    # Pricing levels to filter the search result with: 1 = $, 2 = $$, 3 = $$$, 4 = $$$$.
    b = BusinessSearch(term='', location='Quebec', price=1)
    db = DatabaseDriver()
    db.setup()

    queries = [insert_business_table.format(*to_string(result)) for result in b.get_results()]
    query_to_execute = "BEGIN; \n" + '\n'.join(queries) + "\nCOMMIT;"
    db.execute_query(query_to_execute)

if __name__ == "__main__":
    main()