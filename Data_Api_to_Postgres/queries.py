create_business_schema = """CREATE SCHEMA IF NOT EXISTS yelp;"""

create_business_table = """
CREATE TABLE IF NOT EXISTS yelp.business (
	business_id varchar PRIMARY KEY,
	business_name varchar,
	image_url varchar,
	url varchar,
	review_count int, 
	categories varchar,
	rating float,
	latitude float,
	longitude float,
	price varchar,
	location varchar,
	phone varchar
);
"""

insert_business_table = """INSERT INTO yelp.business VALUES ('{}', '{}', '{}', '{}', {}, '{}', {}, {}, {}, '{}', '{}', '{}')
                        ON CONFLICT (business_id)
                        DO UPDATE SET
                        business_id = EXCLUDED.business_id,
                        business_name = EXCLUDED.business_name,
                        image_url = EXCLUDED.image_url,
                        url = EXCLUDED.url,
                        review_count = EXCLUDED.review_count,
                        categories = EXCLUDED.categories,
                        rating = EXCLUDED.rating,
                        latitude = EXCLUDED.latitude,
                        longitude = EXCLUDED.longitude,
                        price = EXCLUDED.price,
                        location = EXCLUDED.location,
                        phone = EXCLUDED.phone;
                        """