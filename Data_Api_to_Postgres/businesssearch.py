# This is request module of this project
from request import Request
from auth import headers
import json

class BusinessSearch:
    def __init__(self, term, location, price=None):
        self._param = {'term' : term, 'location' : location}
        if price:
            self._param['price'] = price
        self._base_url = 'https://api.yelp.com/v3/businesses/search'
        self._business_list = self._search_business()

    def _search_business(self):
        business_search_request = Request.get_content(url=self._base_url, param=self._param)
        return business_search_request['businesses'] if business_search_request is not None else []

    def _parse_results(self, data):
        # Categories data : 'categories': [{'alias': 'bakeries', 'title': 'Bakeries'}]
        categories = ' '.join([category['title'] for category in data['categories']])

        # Longitude and latitude data :  'coordinates': {'latitude': 45.5232, 'longitude': -73.583459}
        longitude = data['coordinates']['longitude']
        latitude = data['coordinates']['latitude']

        # Location example : 'location': { 'display_address': ['316 Avenue du Mont-Royal E', 'Montreal, QC H2T 1P7', 'Canada']}
        location = ','.join(data['location']['display_address'])

        return {"id" : data['id'], "name" : self._add_escape_character(data['name']), "image_url" : data['image_url'], "url" : data['url'],
                "review_count" : data['review_count'], "categories" : categories, "rating" : data['rating'],
                "latitude" : latitude, "longitude" : longitude, "price" : data['price'], "location" : location,
                "display_phone" : data['display_phone']
                }

    def _add_escape_character(self, data):
        return data.replace("'", "''")

    def get_results(self):
        return [self._parse_results(business) for business in self._business_list]