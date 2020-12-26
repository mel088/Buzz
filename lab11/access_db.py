# this python file will use/read from the database

# built in python3, no need to pip3 install
import sqlite3

# connect to the database
con = sqlite3.connect('database2.db')
cur = con.cursor()

sql = """
select * from users
"""
cur.execute(sql)
results = cur.fetchall()
print('results=',results)
for row in results:
    print('================')
    # the row variable corresponds to the rows of the table that match the select command
    print('row=',row)

    # a tuple is like a list, but with () instead of []
    print('id=', row[0])
    print('username=', row[1])
    print('password=', row[2])
    print('age=', row[3])

sql = """
select * from messages
"""
cur.execute(sql)
results = cur.fetchall()
print('results=',results)
for row in results:
    print('================')
    # the row variable corresponds to the rows of the table that match the select command
    print('row=',row)

    # a tuple is like a list, but with () instead of []
    print('id=', row[0])
    print('sender_id=', row[1])
    print('message=', row[2])
    print('created_at=', row[3])
