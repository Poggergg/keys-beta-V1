import flask
from flask import request, flash, render_template
import flask_login
from execute import CEPLID
from db import userDB, db_ext, msgDB, CDB
import os
from flask_socketio import SocketIO, emit




app = flask.Flask(__name__)
app.secret_key = 'super secret string'
socketio = SocketIO(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'foo@bar.tld': {'password': 'secret'}}

userDB._set("mydb.json")
msgDB._set("mymsgdb.json")


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in userDB._unappend(mode='file'):
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('username')
    if email not in users:
        return "Email not found"

    user = User()
    user.id = email
    return user


@app.route('/')
def landing():
    return flask.render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                 <input type='text' name='email' id='email' placeholder='email'/>
                 <input type='password' name='password' id='password' placeholder='password'/>                 
                 <input type='submit' name='submit'/>
              </form>
               '''

    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/render/<temp>')
def render(temp):
    return flask.render_template(temp)


@app.route('/home')
@flask_login.login_required
def protected():
    return flask.render_template("index.html")


@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if flask.request.method == "GET":
        return flask.render_template("sign-up.html")

    elif flask.request.method == "POST":
        userDB._append(
            request.form["email"], {
                "user": request.form["username"],
                "email": request.form["email"],
                "password": request.form["password"]
            })
        email = request.form["email"]
        if email not in users:
          return "an uncaught exception occured! sorry."
        
        user = User()
        user.id = request.form['username']
        return flask.redirect(flask.url_for('protected'))

# email = request.form.get('username')
#     if email not in users:
#         return "Email not found"

#     user = User()
#     user.id = email
#     return user

@app.route('/exec/<password>/<code>')
def excut(password, code):
  if password == os.environ["pass"]:
    CDB._append(key=code, val=code)
    return f"""<meta property = "og:description" content = "{CEPLID._eval(code)}">"""

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@socketio.event
def my_event(message):
    emit('my response', {'data': 'got it!'})

# we need to convert this js to a python sio thing
# io.on('connection', (socket) => {
#   socket.on('chat message', msg => {
#     io.emit('chat message', msg);
#   });
# });

@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.redirect('/login')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True, port=8080)
