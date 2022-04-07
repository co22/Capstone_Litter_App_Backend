from asyncio.windows_events import NULL
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, current_user, AnonymousUserMixin
import sqlite3, json

app = Flask(__name__)

""" 
Backend for Litter App Project.
Contains functions for user account creation/login, retrieving user data and modifying user data.
"""

# Create a sqlite database at the specified location. (/// = relative path, //// = absolute path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
# Specify the secret key
app.config['SECRET_KEY'] = 'thisissecret'
# Instantiate the database
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Guest User
class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'

# Instantiate and initalize LoginManager
login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.init_app(app)

# Create user class that represents the database table.
# Inherit from UserMixin to use for flask login.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # DO NOT CHANGE 'id' name
    username = db.Column(db.String(30), unique=True)
    score = db.Column(db.Integer)
    petLevel = db.Column(db.Integer)
    petCurrentExp = db.Column(db.Integer)
    petCurrentFood = db.Column(db.Integer)
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
    return User.query.filter(User.id == user_id).first()

# Function index(): Does nothing.
# Arguments: NA
# Returns: NA
@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as {session["username"]}'
    return 'You are not logged in'

# Function getuser(): checks if post request data matches
#                     a user in the database.
# Arguments: NA
# Returns: username
@app.route('/getuser', methods=['POST'])
def getuser():
    data = str(request.get_data(as_text=True))
    global currentUserName
    currentUserName = (request.get_data(as_text=True))
    return data

# Function login(): calls the method to log a user in.
# Arguments: NA
# Returns: getuser() or logout() function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return getuser()

# Function: logout(): logs out a user.
# Arguments: NA
# Returns: logout message
@app.route('/logout')
def logout():
    currentUserName = 'Guest'
    return 'You are now logged out!'

# Function: shows information about the user.
# Arguments: NA
# Returns: the current user's username
@app.route('/home')
def home():
    return 'The current user is ' + current_user.username

# Function: adduser(): add a user to the database
# Arguments: NA
# Returns: the user that was added to the database.
@app.route('/adduser', methods=['POST'])
def adduser():
    data = str(request.get_data(as_text=True))
    newuser = User(username=data, score=0, petLevel=1, petCurrentExp=0, petCurrentFood=0)

    db.session.add(newuser)
    db.session.commit()

    return 'User added: ' + data

# Function: addScore(): add points to the current user's score value
# Arguments: NA
# Returns: User's new score
@app.route('/addscore', methods=['POST'])
def addscore():
    data = str(request.get_data(as_text=True))
    data = int(data)
    user = User.query.filter_by(currentUserName).first()
    score = user.score
    new_score = score + data
    user.score = new_score
    db.session.commit()

    return str(user.score)

# Function: updategoal(): replaces one of the tasks with the new version
# Arguments: <goal num>_<message>_<goal progress>_<goal requirement> OR <goal num>_get OR <goal num>_add_<progress to add>
# Returns: <goal num>_<message>_<goal progress>_<goal requirement>
@app.route('/updateGoal', methods=['POST'])
def updateGoal():
    user = User.query.filter_by(username=currentUserName).first() ## TODO update to work for all users
    data = str(request.get_data(as_text=True))

    # Parse Post data ( requests data fragments are split on underscores )
    data_list = data.split('_') # <-- Funny face lol
    # Goal id
    # Goal description
    # Progress
    # Total Needed

    # Unify requests by using format:
    # "<goal number>_get" to return goal data
    # "<goal number>_add_<progress to add>" to update just the number progress on a goal and return
    update = True
    add = False
    if data_list[1] == "get":
        print("get")
        update = False
    if data_list[1] == 'add':
        print("add")
        update = False
        add = True

    if data_list[0] == str(1):
        if update:
            user.goal1_id = data_list[1]
            user.goal1_progress = data_list[2]
            user.goal1_required = data_list[3]
        if add:
            user.goal1_progress += data_list[2]
        db.session.commit()
        return str(data_list[0]) + "_" + str(user.goal1_id) +  "_" + str(user.goal1_progress) +  "_" + str(user.goal1_required)
    if data_list[0] == str(2):
        if update:
            user.goal2_id = data_list[1]
            user.goal2_progress = data_list[2]
            user.goal2_required = data_list[3]
        if add:
            user.goal2_progress += data_list[2]
        db.session.commit()
        return str(data_list[0]) +  "_" + str(user.goal2_id) +  "_" + str(user.goal2_progress) +  "_" + str(user.goal2_required)
    if data_list[0] == str(3):
        if update:
            user.goal3_id = data_list[1]
            user.goal3_progress = data_list[2]
            user.goal3_required = data_list[3]
        if add:
            user.goal3_progress += data_list[2]
        db.session.commit()
        return str(data_list[0]) +  "_" + str(user.goal3_id) +  "_" + str(user.goal3_progress) +  "_" + str(user.goal3_required)

# Function: getScore(): get the current user's score value
# Arguments: NA
# Returns: Currently logged in user's score
@app.route('/getscore', methods=['POST'])
def getscore():
    user = User.query.filter_by(username=currentUserName).first()
    return str(user.score)
    
# Function: getPetLevel(): get the pet level
# Arguments: NA
# Returns: Pet level
@app.route('/getpetlevel', methods=['POST'])
def getpetlevel():
    user = User.query.filter_by(username=currentUserName).first()
    return str(user.petLevel)

# Function: getCurrentPetExp(): get the pet's current exp
# Arguments: NA
# Returns: Pet current exp value
@app.route('/getpetcurrentexp', methods=['POST'])
def getcurrentpetexp():
    user = User.query.filter_by(username=currentUserName).first()
    return str(user.petCurrentExp)

# Function: getPetFood(): get the pet's current food count
# Arguments: NA
# Returns: Pet food count
@app.route('/getpetcurrentfood', methods=['POST'])
def getpetcurrentfood():
    user = User.query.filter_by(username=currentUserName).first()
    return str(user.petCurrentFood)

# Function: updatePetLevel(): update the pet level
# Arguments: NA
# Returns: Pet level
@app.route('/updatepetlevel', methods=['POST'])
def updatepetlevel():
    data = str(request.get_data(as_text=True))
    data = int(data)
    user = User.query.filter_by(username=currentUserName).first()
    level = user.petLevel
    new_level = level + data
    user.petLevel = new_level
    db.session.commit()

    return str(user.petLevel)

# Function: updatePetExp(): update the pet level
# Arguments: NA
# Returns: Pet current exp
@app.route('/updatepetexp', methods=['POST'])
def updatepetexp():
    data = str(request.get_data(as_text=True))
    data = int(data)
    user = User.query.filter_by(username=currentUserName).first()
    exp = user.petCurrentExp
    new_exp = exp + data
    user.petCurrentExp = new_exp
    db.session.commit()

    return str(user.petCurrentExp)

# Function: updatePetFood(): update the pet level
# Arguments: NA
# Returns: Pet food count
@app.route('/updatepetfood', methods=['POST'])
def updatepetfood():
    data = str(request.get_data(as_text=True))
    data = int(data)
    user = User.query.filter_by(username=currentUserName).first()
    food = user.petCurrentFood
    new_food = food + data
    user.petCurrentFood = new_food
    db.session.commit()

    return str(user.petCurrentFood)

# Function: getLeaderBoard(): format users from database into json format
# Arguments: NA
# Returns: JSON object containing all users in the database
# (Note: The returned JSON object is not sorted by score.)
@app.route('/getleaderboard', methods=['POST'])
def getleaderboard():
    conn = sqlite3.connect('login.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rows = c.execute('''SELECT * FROM user;''').fetchall()
    conn.commit()
    conn.close()

    return json.dumps( [dict(ix) for ix in rows] )


if __name__ == '__main__':
    app.run(debug=True) # Run with flask run --host=0.0.0.0 to connect to android device