Project Goal:
The purpose of this project is to create a reporting tool that reports 
on customer usages queried from database. This reporting tool is a Python 
program using the psycopg2 module to connect to the database.

You have to query the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time? 
3. On which days did more than 1% of requests lead to errors?

How Do I Complete This Project?
To start on this project, you'll need database software (Linux virtual machine) and the 
data (newsdata.sql) to analyze. Put this file into the vagrant directory, which is shared 
with virtual machine.

To load the data, in the terminal use the command 
       psql -d news -f newsdata.sql.

Connect to your database using 
       psql -d news 
and explore the tables using the 
       \dt 
select statements.       

Create first query:
Q1: select title, count(path) as view from articles, log where '/article/' || articles.slug = log.path group by title, path order by view  desc limit 3;

Create view log-count:
create view log_count as select path, count(path) as total from log group by path order by total desc;

Create view authors-count:
create view authors_count as select articles.author as author_id, sum(log_count.total) as total from articles, log_count where log_count.path = '/article/' || articles.slug group by articles.author;

Create second query:
Q2: select authors.name as name, authors_count.total as view from authors, authors_count where authors.id = authors_count.author_id order by view desc;

Create view log-dates:
create view log_dates as select date_trunc('day', time) as log_date, count(status) as total from log group by log_date order by log_date asc;

Create view errors:
create view errors as select date_trunc('day', time) as error_date, count(status) as error_total from log where status = '404 NOT FOUND' group by error_date order by error_date asc;

Create third query:
Q3: select log_dates.log_date as day, cast(errors.error_total as float) / cast(log_dates.total as float) as percent from log_dates, errors where log_dates.log_date = errors.error_date group by day, error_total, total having cast(errors.error_total as float) / cast(log_dates.total as float) >= .01 order by day asc;

Create newsdata.py file.

In terminal run the newsdata.py file in news directory using the command
          python newsdata.py

Output:
By the end the output will look like this

Most popular three articles of all time: 
---------------------------------------- 
Candidate is jerk, alleges rival -- 338647  views
Bears love berries, alleges bear -- 253801  views
Bad things gone, say good people -- 170098  views
 
Most popular article authors of all time: 
----------------------------------------- 
Ursula La Multa -- 507594  views
Rudolf von Treppenwitz -- 423457  views
Anonymous Contributor -- 170098  views
Markoff Chaney -- 84557  views
 
Dates with more than 1% error rate:
-----------------------------------
July 17 , 2016 --  2.26% errors
