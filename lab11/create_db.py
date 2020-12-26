# this python file just creates the table schemas,
# and inserts some dummy data
# built in python3, no need to pip3 install
import sqlite3
# connect to the database
con = sqlite3.connect('database6.db')
cur = con.cursor()

#create table users
sql = '''
create table users (
    id integer primary key,
    username text not null unique,
    password text not null,
    age integer
    );
'''
#cur.execute(sql)
#con.commit

#create table messages
sql = '''
create table messages (
    id integer primary key,
    sender_id integer not null,
    message text not null,
    created_at timestamp not null default current_timestamp
    );
'''
#cur.execute(sql)
#con.commit

#insert into users
sql = '''
insert into users (username, password, age) values
    ('melaknee_08', 'abc', 20),
    ('berleezy', 'roastme', 28),
    ('theofficialtravis', 'travisscottyes', 18);
'''
#cur.execute(sql)
#con.commit

#insert into messages
sql = '''
insert into messages (sender_id, message) values
    (3, 'Gimme the loot'),
    (1, 'It is nap time.'),
    (2, 'Look at my boy, Jimmy.'),
    (3, 'Sicko MODE'),
    (2, 'What is good guys');
'''
cur.execute(sql)

con.commit()
"""
sql = '''
select * from messages;
'''
cur.execute(sql)
results = cur.fetchall()
print('results=',results)

sql = '''
select * from users;
'''
cur.execute(sql)
results = cur.fetchall()
print('results=',results)
"""
