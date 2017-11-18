#!/usr/bin/env python2.7
#  Queries to Analyze News Data
# Import database
import psycopg2

DBNAME = "news"


def connect(db_name):
    """Connect to the PostgreSQL database.  Returns a database connection.

       Args:
          db_name - specifies the name of the database

       Returns
          db, c - A two element tuple. The first element is a connection
                  to the database. The second element is a cursor for the
                  database connection."""
    try:
        db = psycopg2.connect("dbname={}".format('news'))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to database")


def popular_articles():
    """Returns the top 3 most popular articles"""
    db = psycopg2.connect("dbname=news")
    """Connect to news database."""
    c = db.cursor()
    """Open a cursor to perform database operation."""
    query = """select title, count(path) as view from articles, log 
    where '/article/' || articles.slug = log.path group by title, path 
    order by view  desc limit 3;"""
    """The cursor runs query and fetches result."""
    c.execute(query)
    """Execute query using cursor."""
    rows = c.fetchall()
    print "Most popular three articles of all time: "
    print "---------------------------------------- "
    for row in rows:
        print row[0], "--", row[1], " views"
    db.close()


def popular_authors():
    # Returns a list of the most popular authors
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = """select authors.name as name, authors_count.total as view from
    authors, authors_count where authors.id = authors_count.author_id
    order by view desc;"""
    c.execute(query)
    authors = c.fetchall()
    print " "
    print "Most popular article authors of all time: "
    print "----------------------------------------- "
    for author in authors:
        print author[0], "--", author[1], " views"
    db.close()


def error_days():
    """Remove all the match records from the database."""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = """select log_dates.log_date as day, 
    cast(errors.error_total as float) / cast(log_dates.total as float) 
    as percent from log_dates, errors where
    log_dates.log_date = errors.error_date group by day, error_total, total
    having cast(errors.error_total as float) / cast(log_dates.total
    as float) >= .01 order by day asc;"""
    c.execute(query)
    errors = c.fetchall()
    print " "
    print "Dates with more than 1% error rate:"
    print "-----------------------------------"
    for error in errors:
        print error[0].strftime("%B %d , %Y"), "--",\
            "{: .2%}".format(error[1]), "errors"

    db.close()


if __name__ == '__main__':
    popular_articles()
    popular_authors()
    error_days()
