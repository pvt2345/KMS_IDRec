# !/usr/bin/python
import pymysql.cursors
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connect to the database.
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='CIST#2o!7',
                             db='qlvb',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

print(" =====> Connect successful!")

try:
    with connection.cursor() as cursor:
        # SQL
        sql = "SELECT * FROM document "

        # Execute query.
        cursor.execute(sql)

        print("cursor.description: ", cursor.description)

        print()

        for row in cursor:
            print(row)

finally:
    # Close connection.
    connection.close()


