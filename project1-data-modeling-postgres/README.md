# Data Modeling with Postgres
## Data Engineering with Microsoft Azure

## Project Description
In this project, I have defined fact and dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL.

## Background on the project
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Running the project files
You can run the project files by running the following commands in the terminal:
$ python create_table.py
$ python etl.py


## Explanation of all the files in the repository
* create_tables.py 
<br>drops and creates your tables. You run this file to reset your tables before each time you run your ETL scripts.

* etl.py 
<br>Reads and processes files from song_data and log_data and loads them into your tables. You can fill this out based on your work in the ETL notebook.

* sql_queries.py 
<br>Contains all your sql queries, and is imported into the last three files above.

* test.ipynb 
<br>Displays the first few rows of each table to let you check your database.

* etl.ipynb 
<br>Reads and processes a single file from song_data and log_data and loads the data into your tables. This notebook contains detailed instructions on the ETL process for each of the tables.

## State and justify your database schema design and ETL pipeline
songplays is the Fact table in our design.
<br><br>
All other tables (users, songs, artists, and time) are the Dimension tables in our design. These dimension tables are connected to the fact table through their individual primary (users.user_id, songs.song_id, artists.artist_id, and time.start_time) keys.
<br><br>
ETL work is done in 2 steps. First, we load the data from song files (song_data) to populate songs and artists tables. Second, we load data from log files (log_data) to populate users, time, and songplays tables.
<br><br>
With the ETL pipeline completed, you should have a much simpler database schema and a working ETL pipeline that we can use to load the data into our database continuously with some type cron jobs or some even driven mechanism. Our SQL joins to create a report or extract the data becomes much simpler due to the star schema design. Reading of the data is much faster and that is a huge benefit of the star schema.