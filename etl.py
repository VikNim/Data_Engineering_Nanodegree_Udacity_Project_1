import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    df = pd.DataFrame()
    
    data = pd.read_json(filepath, lines=True)
    df = df.append(data, ignore_index = True)

    # insert song record
    song_data = (df['song_id'].tolist()[0], df['title'].tolist()[0], df['artist_id'].tolist()[0], df['year'].tolist()[0], df['duration'].tolist()[0])
#     print(type(df['song_id']))
#     print(df['song_id'])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = (df['artist_id'].tolist()[0], df['artist_name'].tolist()[0], df['artist_location'].tolist()[0], df['artist_latitude'].tolist()[0], df['artist_longitude'].tolist()[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    df = pd.DataFrame()
    
    data = pd.read_json(filepath, lines=True)
    df = df.append(data, ignore_index = True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    hour = list(t.dt.hour)
    day = list(t.dt.day)
    week = list(t.dt.weekofyear)
    month = list(t.dt.month)
    year = list(t.dt.year)
    weekday = list(t.dt.weekday)
    start_time = list(t) 
    
    # insert time data records
    column_labels = ('start_time','hour', 'day', 'week', 'month','year', 'weekday')
    time_df = pd.DataFrame({
                                "start_time": start_time,
                                "hour"      : hour,
                                "day"       : day,
                                "week"      : week,
                                "month"     : month,
                                "year"      : year,
                                "weekday"   : weekday
                            })

    for _, row in time_df.iterrows():
        time_data = (row['start_time'], row['hour'], row['day'], row['week'], row['month'], row['year'], row['weekday'])
        cur.execute(time_table_insert, time_data)

    # load user table
    user_df = pd.DataFrame(df[['userId', 'firstName', 'lastName', 'gender', 'level']])

    # insert user records
    for _, row in user_df.iterrows():
        user_data = row['userId'], row['firstName'], row['lastName'], row['gender'], row['level']
        cur.execute(user_table_insert, user_data)

    # insert songplay records
    for _, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row['song'], row['artist'], row['length']))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
            start_time = pd.to_datetime(row['ts'], unit='ms')
            userId = row['userId']
            level = row['level']
            sessionId = row['sessionId']
            location = row['location']
            userAgent = row['userAgent']

            songplay_data = (start_time,userId,level,songid,artistid,sessionId,location, userAgent)
            # insert songplay record
            cur.execute(songplay_table_insert, songplay_data)
        else:
            songid, artistid = None, None

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    if 'song_data' in filepath:
        all_files = sorted([s for s in all_files if '/song_data/' in s and 'ipynb_checkpoints' not in s])
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()