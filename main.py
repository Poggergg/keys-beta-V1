import flask
import flask_login

app = flask.Flask(__name__)
app.secret_key = 'super secret string'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'foo@bar.tld': {'password': 'secret'}}
class User(flask_login.UserMixin):
  pass


@login_manager.user_loader
def user_loader(email):
  if email not in users:
    return 

    user = User()
    user.id = email

    return user

@login_manager.request_loader
def request_loader(request):
  email = request.form.get('email')
  if email not in users:
    return
    user = User()
    user.id = email
    return user

@app.route('/', methods=['GET', 'POST'])
def login():
  if flask.request.method == 'GET':
    return flask.render_template("login.html")
    email = flask.request.form['email']

    if flask.request.form['password'] == users[email]['password']:
      user = User()
      user.id = email
      flask_login.login_user(user)
      return flask.redirect(flask.url_for('protected'))

      return 'Bad login'

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
  if flask.request.method == 'GET':
    return flask.render_template("login.html")
    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
      user = User()
      user.id = email
      flask_login.login_user(user)
      return flask.redirect(flask.url_for('protected'))
      
  return 'Bad login'

@app.route('/@me')
  
@flask_login.login_required
def protected():
  return flask.render_template("base.html", u = flask_login.current_user.id)

@app.route('/logout')
def logout():
  flask_login.logout_user()
  return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
  return 'Unauthorized'

app.run(host="0.0.0.0", port=8080, debug=True)