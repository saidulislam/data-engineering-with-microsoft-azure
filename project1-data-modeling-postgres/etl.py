import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This function is used to read the file in the filepath (data/song_data)
    to get the song and artist info and used to populate the song and artist dim tables.

    Arguments:
        cur: the cursor object. 
        filepath: log data file path. 

    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath , lines=True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This function reads the log file, filters the data by NextSong action,
    converts the timestamp column to datetime, inserts time data records,
    loads user table, inserts user records, and inserts songplay records.
    
    Arguments:
        cur: the cursor object. 
        filepath: log data file path. 

    Returns:
        None
    """
    # open log file
    df = pd.read_json(filepath , lines=True)

    # filter by NextSong action
    df = df.query('page == "NextSong"')

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    # idea from https://knowledge.udacity.com/questions/899220
    time_data = [[x, x.hour, x.day, x.week, x.month, x.year, x.dayofweek] for x in t]
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId","firstName","lastName","gender","level"]].drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (t[index],row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This function takes the cursor, connection, filepath and function as input and processes the data.
    It gets all the files matching the extension from the directory.
    It gets the total number of files found.
    It iterates over the files and processes the data.
    
    Arguments:
        cur: the cursor object. 
        conn: the connection object.
        filepath: log data file path.
        func: function to process the data.

    Returns:
        None
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
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