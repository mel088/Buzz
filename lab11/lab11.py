from flask import Flask, render_template, send_from_directory, request, make_response
app = Flask(__name__)
import sqlite3
#import pandas as pd

####username='melaknee_08'
##@app.route('/')

def is_logged_in(cur, username, password):
    sql = '''
        SELECT username,password FROM users where username=? and password=?;
    '''
    cur.execute(sql, (username,password))
    rows = cur.fetchall()

    if len(list(rows))==0:
        return False
    else:
        return True

@app.route('/')
def root():
    #return render_template('index.html')
    logged_in=True
    #username='melaknee_08'
    con = sqlite3.connect('database2.db')
    cur = con.cursor()
    sql = sql = '''
        SELECT sender_id,message,created_at,id FROM messages;
    '''
    cur.execute(sql)
    rows = cur.fetchall()
    messages = []
    for row in rows:
        sql = '''
            SELECT username FROM users WHERE id=?
        '''
        cur.execute(sql, (row[0],))
        username_rows = cur.fetchall()
        for username_row in username_rows:
            username = username_row[0]
        messages.append({
            'text' : row[1],
            'username' : username,
            'created_at' : row[2],
            'sender_id' : row[0],
            'id' : row[3],
        })
    messages.reverse()
        
        

    '''
    messages = [
        {'text' : 'meow', 'username' : 'Gary'},
        {'text' : 'gwahhh', 'username' : 'Appa'},
        {'text' : 'ee ee', 'username' : 'Momo'},
    ]
    '''

    if logged_in:
        return render_template(
            'index.html',
            username=request.cookies.get('username'),
            messages=messages
            )
    else:
        return render_template(
            'index.html',
            messages=messages
            )

@app.route('/login', methods=['get','post'])
def login():
    #if request.args.get('username'):
    if request.form.get('username'):
        
        # check whether the username/password is correct in the db
        
        con = sqlite3.connect('database2.db')
        cur = con.cursor()
        login_successful = is_logged_in(
            cur=cur,
            username=request.form.get('username'),
            password=request.form.get('password'),
        )
        """
        sql = '''
            SELECT username,password FROM users where username=? and password=?;
        '''
        cur.execute(sql, (request.form.get('username'), request.form.get('password')))
        rows = cur.fetchall()
        if len(list(rows))==0:
            login_successful=False
        else:
            login_successful=True
            """

        # check the database to see if their login credentials are correct
        #username = 'mike'
        #password = '12345'
        #if request.args.get('username')==username and request.args.get('password')==password:  
        #if request.form.get('username')==username and request.form.get('password')==password:  
        if login_successful:
            # set the cookie value
            res = make_response(render_template(
                'login.html',
                login_successful=True,
                username=request.form.get('username')
                ))
            #res.set_cookie('username',request.args.get('username'))
            res.set_cookie('username',request.form.get('username'))
            res.set_cookie('password',request.form.get('password'))
            return res
        else:
            return render_template(
                'login.html',
                login_unsuccessful=True
                )
    else:
        return render_template(
                'login.html',
                login_default=True
                )


@app.route('/logout')
def logout():
    res = make_response(render_template(
        'logout.html',
        ))
    res.set_cookie('username','',expires=0)
    res.set_cookie('password','',expires=0)
    return res


        #insert into messages (message) values
            #(?, ?, ?, ?);
        #'''

@app.route('/create_user', methods=['get','post'])
def create_user():
    #if request.args.get('username'):
    if request.form.get('username'):
        con = sqlite3.connect('database2.db')
        cur = con.cursor()
        username = request.form['username']
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cur.fetchone() is not None:
            return render_template(
                'create_user.html',
                user_already_exists=True
                )
        else:
            sql='''
            INSERT INTO users (username,password) VALUES
                (?, ?);
            '''
            cur.execute(sql, (request.form.get('username'), request.form.get('password')))
            con.commit()
            #rows = cur.fetchall()
            password=request.form.get('password')
            password2=request.form.get('password2')
            if password==password2:
                create_user_successful=True
            else:
                create_user_successful=False
            

            # check the database to see if their login credentials are correct
            #username = 'mike'
            #password = '12345'
            #if request.args.get('username')==username and request.args.get('password')==password:  
            #if request.form.get('username')==username and request.form.get('password')==password:  
            if create_user_successful:
                # set the cookie value
                res = make_response(render_template(
                    'create_user.html',
                    create_user_successful=True,
                    username=request.form.get('username')
                    ))
                #res.set_cookie('username',request.args.get('username'))
                res.set_cookie('username',request.form.get('username'))
                res.set_cookie('password',request.form.get('password'))
                return res
            else:
                return render_template(
                    'create_user.html',
                    create_user_unsuccessful=True
                    )
    else:
        return render_template(
                'create_user.html',
                create_user_default=True
                )

@app.route('/create_message', strict_slashes=False, methods=['get','post'])
def create_message():
    logged_in=True
    if request.form.get('message'):
        con = sqlite3.connect('database2.db')
        cur = con.cursor()
        sql = sql = '''
            SELECT id,username FROM users;
        '''
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            if row[1] ==request.cookies.get('username'):
                sender_id = row[0]
            print(row)
        message = request.form.get('message')
        con = sqlite3.connect('database2.db')
        cur = con.cursor()
        sql = '''
        INSERT INTO messages (sender_id, message) VALUES
            (?, ?);
        '''
        cur.execute(sql, (sender_id, message,))
        con.commit()
        rows = cur.fetchall()
        if len(message)==0:
            message_successful=False
        else:
            message_successful=True
            
        if message_successful:
            # set the cookie value
            res = make_response(render_template(
                'create_message.html',
                message_successful=True,
                username = request.cookies.get('username'),
                password = request.cookies.get('password'),
                message=request.form.get('message')
                ))
            return res
        else:
            return render_template(
                'create_message.html',
                username = request.cookies.get('username'),
                password = request.cookies.get('password'),
                message_unsuccessful=True
                )
    else:
        res = make_response(render_template(
            'create_message.html',
            username = request.cookies.get('username'),
            password = request.cookies.get('password'),
            message_default=True
            ))
        return res

@app.route('/delete_message/<id>')
def delete_message(id):
    con = sqlite3.connect('database2.db')
    cur = con.cursor()
    if is_logged_in(
        cur=cur,
        username=request.cookies.get('username'),
        password=request.cookies.get('password'),
    ):
        sql='''
        DELETE FROM messages WHERE id=?;
        '''
        cur.execute(sql, (id,))
        con.commit()
        res = make_response(render_template(
            'delete_message.html',
            username = request.cookies.get('username'),
            password = request.cookies.get('password'),
            ))
        return res

@app.route('/edit_message/<id>', methods=['get','post'])
def edit_message(id):
    logged_in=True
    if request.form.get('edit_message'):
        message = request.form.get('edit_message')
        con = sqlite3.connect('database2.db')
        cur = con.cursor()
        sql='''
        UPDATE messages SET message=? WHERE id=?;
        '''
        cur.execute(sql, (message, id))
        con.commit()
        rows = cur.fetchall()
        if len(message)==0:
            edit_message_successful=False
        else:
            edit_message_successful=True
            
        if edit_message_successful:
            # set the cookie value
            res = make_response(render_template(
                'edit_message.html',
                edit_message_successful=True,
                username = request.cookies.get('username'),
                password = request.cookies.get('password'),
                id=id,
                message=request.form.get('edit_message')
                ))
            return res
        else:
            return render_template(
                'edit_message.html',
                username = request.cookies.get('username'),
                password = request.cookies.get('password'),
                edit_message_unsuccessful=True
                )
    else:
        res = make_response(render_template(
            'edit_message.html',
            username = request.cookies.get('username'),
            password = request.cookies.get('password'),
            edit_message_default=True
            ))
        return res
"""
@app.route('/edit_message/<id>', methods=['get','post'])
def edit_message(id):
    logged_in=True
    if request.form.get('edit_message'):
        con = sqlite3.connect('database2.db')
        cur = con.cursor()
        #sql = sql = '''
           # SELECT FROM users WHERE id=?;
        #'''
        sql = sql = '''
            SELECT id,username FROM users;
        '''
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            if row[1] ==request.cookies.get('username'):
                id = row[0]
                cur.execute(sql)
                message = request.form.get('edit_message')
                con = sqlite3.connect('database2.db')
                cur = con.cursor()
                sql = '''
                UPDATE messages SET message=? WHERE id='$id';
                    (?);
                '''
                cur.execute(sql)
                con.commit()
                rows = cur.fetchall()
                if len(message)==0:
                    edit_message_successful=False
                else:
                    edit_message_successful=True
            
                if edit_message_successful:
                    if request.method == 'post':
                    # set the cookie value
                        res = make_response(render_template(
                            'edit_message.html',
                            edit_message_successful=True,
                            username = request.cookies.get('username'),
                            password = request.cookies.get('password'),
                            message=request.form.get('edit_message')
                            ))
                        return res
                else:
                    return render_template(
                        'edit_message.html',
                        username = request.cookies.get('username'),
                        password = request.cookies.get('password'),
                        edit_message_unsuccessful=True
                        )
    else:
        res = make_response(render_template(
            'edit_message.html',
            username = request.cookies.get('username'),
            password = request.cookies.get('password'),
            edit_message_default=True
            ))
        return res
"""    

@app.route('/delete_user/<username>')
def delete_user(username):
    con = sqlite3.connect('database2.db')
    cur = con.cursor()
    if is_logged_in(
        cur=cur,
        username=request.cookies.get('username'),
        password=request.cookies.get('password'),
    ):
    #get username from cookies
        sql='''
        DELETE FROM users WHERE username=?;
        '''
        cur.execute(sql, (username,))
        con.commit()
        res = make_response(render_template(
            'delete_user.html',
            ))
        res.set_cookie('username','',expires=0)
        res.set_cookie('password','',expires=0)
        return res
        
@app.route('/user/<username>')
def user(username):
    return render_template(
        'user.html',
        username=username
        )

@app.route('/static/<path>')
def static_directory(path):
    return send_from_directory('static',path)

@app.errorhandler(404)
def error_message(e):
    return '404: NOT FOUND'

#app.run(host='0.0.0.0')
app.run()
#flask run --host=0.0.0.0
