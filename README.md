# Data_Engineering_Nanodegree_Udacity
The purpose of this project is to implement a basic, simple ETL process for SPRKLIFLY.
We are implementing a star schema database using PostgreSQL database and Python 3.

Project Files:
i)   create_tables: This files makes the database setup by creating sparklifly database schema, 
                    creating tables in database schema and setting necessary constraint for each table.

ii)  etl.py:  This file is the backbone of project.We are extracting data from files, transforming the values
              and loading the values in database with use of this file.

iii) sql_queries: This files provides sql querie for all the operations such as create table, insert a row etc.

Database Design:<br>
<img src="https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/33760/1591881849/Song_ERD.png" />
<br>
To run this project, download the data place all the files in one folder. Run create_tables.py first and then etl.py.

Places to improvements : There is way to bulk insert intead of one by one, I didn't implement it yet since I had a limited time.You can try to implement it.
