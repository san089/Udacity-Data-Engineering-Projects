import configparser
from pathlib import Path
from businesssearch import BusinessSearch
from queries import create_business_schema, create_business_table, insert_business_table

config = configparser.ConfigParser()
config.read_file(open(f"{Path(__file__).parents[0]}/config.cfg"))

api_key = config['KEYS']['API_KEY']
headers = {'Authorization': 'Bearer %s' % api_key}


def main():

    # Pricing levels to filter the search result with: 1 = $, 2 = $$, 3 = $$$, 4 = $$$$.
    b = BusinessSearch(term='', location='Montreal', price=1)
    queries = 
    for result in b.get_results():
        result = [str(value) for value in result.values()]
        print(insert_business_table.format(*result))


if __name__ == "__main__":
    main()