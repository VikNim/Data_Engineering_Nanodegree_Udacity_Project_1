# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays CASCADE"
user_table_drop = "DROP TABLE IF EXISTS users CASCADE"
song_table_drop = "DROP TABLE IF EXISTS songs CASCADE"
artist_table_drop = "DROP TABLE IF EXISTS artists CASCADE"
time_table_drop = "DROP TABLE IF EXISTS time CASCADE"

# CREATE TABLES

user_table_create = ("CREATE TABLE IF NOT EXISTS users (user_id int PRIMARY KEY," + 
                     " first_name varchar, last_name varchar,gender varchar, level varchar)")

artist_table_create = ("CREATE TABLE IF NOT EXISTS artists (artist_id varchar PRIMARY KEY, " + 
                       "name varchar, location varchar, latitude numeric, longitude numeric)")

song_table_create = ("CREATE TABLE IF NOT EXISTS songs (song_id varchar PRIMARY KEY, title " + 
                     "varchar, artist_id varchar, year int, duration numeric, FOREIGN KEY"+
                     "(artist_id) REFERENCES artists(artist_id))")

time_table_create = ("CREATE TABLE IF NOT EXISTS time (start_time timestamp,hour int, day int," + 
                     " week int, month int,year int, weekday varchar)")

songplay_table_create = ("CREATE TABLE IF NOT EXISTS songplays (songplay_id SERIAL PRIMARY KEY," +
                         " start_time timestamp, user_id int, level varchar, song_id varchar," +
                         " artist_id varchar, session_id int, location varchar, user_agent varchar," +
                         " FOREIGN KEY(user_id) REFERENCES users(user_id)," +
                         " FOREIGN KEY(song_id) REFERENCES songs(song_id)," +
                         " FOREIGN KEY(artist_id) REFERENCES artists(artist_id))")

# INSERT RECORDS

songplay_table_insert = (" INSERT INTO songplays(start_time, user_id, level, song_id, artist_id," +
                         " session_id, location, user_agent) values(%s,%s,%s,%s,%s,%s,%s,%s) " + 
                         "ON CONFLICT (songplay_id) DO NOTHING")

user_table_insert = ("INSERT INTO users(user_id,first_name,last_name,gender,level) " +
                     "values(%s,%s,%s,%s,%s) ON CONFLICT(user_id) DO NOTHING")

song_table_insert = ("INSERT INTO songs(song_id, title, artist_id, year, duration) " +
                     "values(%s,%s,%s,%s,%s) ON CONFLICT(song_id) DO NOTHING")

artist_table_insert = ("INSERT INTO artists(artist_id, name, location, latitude, " +
                       "longitude) values(%s,%s,%s,%s,%s) ON CONFLICT(artist_id) DO NOTHING")

time_table_insert = ("INSERT INTO time(start_time,hour, day, week, month,year, " +
                     "weekday) values(%s,%s,%s,%s,%s,%s,%s)")

# FIND SONGS

song_select = ("""select b.song_id, a.artist_id from songs b, artists a where b.title=%s and a.name=%s and b.duration=%s and b.artist_id=a.artist_id""")

# QUERY LISTS

create_table_queries = [user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, song_table_drop, user_table_drop, artist_table_drop, time_table_drop]