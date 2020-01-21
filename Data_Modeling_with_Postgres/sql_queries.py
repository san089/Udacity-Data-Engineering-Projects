# DROP TABLES

songplay_table_drop = "DROP TABLE  IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS  users"
song_table_drop = "DROP TABLE IF EXISTS  songs"
artist_table_drop = "DROP TABLE  IF EXISTS artists"
time_table_drop = "DROP TABLE  IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays(
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

user_table_create = ("""CREATE TABLE IF NOT EXISTS  users(
	user_id  int CONSTRAINT users_pk PRIMARY KEY,
	first_name  varchar,
	last_name  varchar,
	gender  char(1),
	level varchar
)""")

song_table_create = ("""CREATE TABLE  IF NOT EXISTS songs(
	song_id varchar CONSTRAINT songs_pk PRIMARY KEY,
	title  varchar,
	artist_id  varchar REFERENCES artists (artist_id),
	year  int,
	duration  float
)""")

artist_table_create = ("""CREATE TABLE  IF NOT EXISTS artists(
	artist_id  varchar CONSTRAINT artist_pk PRIMARY KEY,
	name  varchar,
	location  varchar,
	latitude  decimal(9,6),
	longitude  decimal(9,6)
)""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS  time(
	start_time  timestamp CONSTRAINT time_pk PRIMARY KEY,
	hour  int,
	day  int,
	week   int,
	month  int,
	year   int,
	weekday varchar
)""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )
""")

user_table_insert = ("""INSERT INTO users VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id) DO NOTHING
""")

song_table_insert = ("""INSERT INTO songs VALUES (%s, %s, %s, %s, %s) ON CONFLICT (song_id) DO NOTHING
""")

artist_table_insert = ("""INSERT INTO artists VALUES (%s, %s, %s, %s, %s) ON CONFLICT (artist_id) DO NOTHING
""")

time_table_insert = ("""INSERT INTO time VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (start_time) DO NOTHING
""")

# FIND SONGS

song_select = ("""
    SELECT song_id, artists.artist_id
    FROM songs JOIN artists ON songs.artist_id = artists.artist_id
    WHERE songs.title = %s
    AND artists.name = %s
    AND songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]