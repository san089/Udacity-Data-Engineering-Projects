# DROP TABLES

songplay_table_drop = "DROP TABLE  IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS  users"
song_table_drop = "DROP TABLE IF EXISTS  songs"
artist_table_drop = "DROP TABLE  IF EXISTS artists"
time_table_drop = "DROP TABLE  IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE songplays(
	songplay_id varchar,
	start_time timestamp REFERENCES time (start_time),
	user_id int REFERENCES users (user_id),
	level varchar,
	song_id varchar REFERENCES songs (song_id),
	artist_id varchar REFERENCES artists (artist_id),
	session_id int,
	location varchar,
	user_agent text
)""")

user_table_create = ("""CREATE TABLE users(
	user_id  int CONSTRAINT users_pk PRIMARY KEY,
	first_name  varchar,
	last_name  varchar,
	gender  char(1),
	level varchar
)""")

song_table_create = ("""CREATE TABLE songs(
	song_id varchar CONSTRAINT songs_pk PRIMARY KEY,
	title  varchar,
	artist_id  varchar,
	year  int,
	duration  float
)""")

artist_table_create = ("""CREATE TABLE artists(
	artist_id  varchar CONSTRAINT artist_pk PRIMARY KEY,
	name  varchar,
	location  varchar,
	latitude  decimal(9,6),
	longitude  decimal(9,6)
)""")

time_table_create = ("""CREATE TABLE time(
	start_time  timestamp CONSTRAINT time_pk PRIMARY KEY,
	hour  int,
	day  int,
	week   int,
	month  int,
	year   int,
	weekday int
)""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )
""")

user_table_insert = ("""INSERT INTO users VALUES (%s, %s, %s, %s, %s)
""")

song_table_insert = ("""INSERT INTO songs VALUES (%s, %s, %s, %s, %s) ON CONFLICT (song_id) DO NOTHING
""")

artist_table_insert = ("""INSERT INTO artists VALUES (%s, %s, %s, %s, %s)
""")


time_table_insert = ("""INSERT INTO time VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""INSERT INTO songplays VALUES ()
""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]