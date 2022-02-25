import abc
from posixpath import split
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from markupsafe import escape

app = Flask(__name__)

### Current functionality: Currently returns a successful login message to a hard-coded user in the database.
### Logout by changing the url path to http://.../logout

# Create a sqlite database at the specified location. (/// = relative path, //// = absolute path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/sqlite/login.db'
# Specify the secret key
app.config['SECRET_KEY'] = 'thisissecret'
# Instantiate the database
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Instantiate and initalize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Create user class that represents the database table.
# Inherit from UserMixin to use for flask login.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # DO NOT CHANGE 'id' name
    username = db.Column(db.String(30), unique=True)
    score = db.Column(db.Integer)
    goal1_id = db.Column(db.String(30))
    goal2_id = db.Column(db.String(30))
    goal3_id = db.Column(db.String(30))
    goal1_progress = db.Column(db.Integer)
    goal2_progress = db.Column(db.Integer)
    goal3_progress = db.Column(db.Integer)
    goal1_required = db.Column(db.Integer)
    goal2_required = db.Column(db.Integer)
    goal3_required = db.Column(db.Integer)

# load_user(): loads a user object from the database given a user_id.
# Arguments: user_id
# Returns: object from SQLAlchemy representing row number that matches the user_id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Function index(): logs in a user.
# Arguments: NA
# Returns: login message
@app.route('/')
def index():
    user = User.query.filter_by(username='Test').first()
    login_user(user)
    return 'You are now logged in!'

# Function getuser(): checks if post request data matches
#                     a user in the database.
# Arguments: NA
# Returns: Successful login message and username.
@app.route('/getuser', methods=['POST'])
def getuser():

    data = str(request.get_data(as_text=True))
    user = User.query.filter_by(username=data).first()
    login_user(user)
    return data

# Function login(): calls the method to log a user in.
# Arguments: NA
# Returns: getuser() or logout() function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return getuser()
    else:
        return logout()

# Function: logout(): logs out a user.
# Arguments: NA
# Returns: logout message
# @login_required decorator protects the page from users who are not logged in
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out!'

# Function: shows information about the user.
# Arguments: NA
# Returns: the current user's username
@app.route('/home')
@login_required
def home():
    return 'The current user is ' + current_user.username

# Function: adduser(): add a user to the database
# Arguments: NA
# Returns: the user that was added to the database.
@app.route('/adduser', methods=['POST'])
def adduser():
    data = str(request.get_data(as_text=True))
    newuser = User(username=data, score=0)

    db.session.add(newuser)
    db.session.commit()

    return 'User added' + data

# Function: addScore(): add points to the current user's score value
# Arguments: NA
# Returns: User's new score
@app.route('/addscore', methods=['POST'])
def addscore():
    data = str(request.get_data(as_text=True))
    data = int(data)
    user = User.query.filter_by(username=current_user.username).first()
    score = user.score
    new_score = score + data
    user.score = new_score
    db.session.commit()

    return str(user.score)

# Function: updategoal(): replaces one of the tasks with the new version
# Arguments: <goal num>_<message>_<goal progress>_<goal requirement> OR <goal num>_get
# Returns: <goal num>_<message>_<goal progress>_<goal requirement>
@app.route('/updateGoal', methods=['POST'])
def updategoal():
    user = User.query.filter_by(username=current_user.username).first()
    data = str(request.get_data(as_text=True))

    # Parse Post data ( requests data fragments are split on underscores )
    data_list = data.split('_') # <-- Funny face lol
    # Goal id
    # Goal description
    # Progress
    # Total Needed

    # Unify requests by using format "<goal number>_get" to return goal data
    update = True
    if data_list[1] == "get":
        update = False

    match data_list[0]:
        case 1:
            if update:
                user.goal1_id = data_list[1]
                user.goal1_progress = data_list[2]
                user.goal1_required = data_list[3]
                db.session.commit()
            return data_list[0] + "_" + user.goal1_id +  "_" + user.goal1_progress +  "_" + user.goal1_required
        case 2:
            if update:
                user.goal2_id = data_list[1]
                user.goal2_progress = data_list[2]
                user.goal2_required = data_list[3]
                db.session.commit()
            return data_list[0] +  "_" + user.goal2_id +  "_" + user.goal2_progress +  "_" + user.goal2_required
        case 3:
            if update:
                user.goal3_id = data_list[1]
                user.goal3_progress = data_list[2]
                user.goal3_required = data_list[3]
                db.session.commit()
            return data_list[0] +  "_" + user.goal3_id +  "_" + user.goal3_progress +  "_" + user.goal3_required

if __name__ == '__main__':
    app.run(debug=True) # Run with flask run --host=0.0.0.0 to connect to android device
    