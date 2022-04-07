Litter App - Pickup Pets

============================================================================================================================================

Overview:

The focus of the Litter App Project is to gamify litter/trash pickup through the use of an android app. The main app includes: a virtual pet that users can feed and level up, a map that allows the user to view their current location as they pick up litter, a camera and labeling screen to take pictures of and identify litter, a goal screen to motivate users to complete certain tasks and allow users to keep track of their progress, and a leaderboard so users can compete with others.

The backend of the Litter App Project handles user account creation, login, and data. This includes scores, goals, and pet progress for each player. This data is stored in "login.db".

============================================================================================================================================

Prequisites:

Python 3.7+: https://www.python.org/
Flask: https://flask.palletsprojects.com/en/2.1.x/

============================================================================================================================================

Installation:

Clone the github repository: https://github.com/co22/Capstone_Litter_App_Backend
For flask installation, see: https://flask.palletsprojects.com/en/2.1.x/installation/#

- Dependencies can be installed using a package manager (for example, pip)
- Dependencies should be installed when in the virtual environment. If you encounter problems with venv, they can be installed on your individual device.
- To activate the virtual environment (venv):
    - Navigate to the venv/Scripts or venv/bin folder.
    - Run the command (". activate") to activate the virtual environment.
        (Note: this was done in a bash terminal; powershell will be slightly different. See flask installation documentation)
    - "(venv)" should appear above your username when the virtual environment has been successfully activated.

============================================================================================================================================

Running:

To run the server on your device:

- Use the command "flask run --host=0.0.0.0" (Note: the "--host=0.0.0.0" flag allows other devices such as android tablets to connect to it)
- To close the server: CTRL/command + C

To connect to the server from the android app:

- In the ConnectionInfo.java file, modify the "address" variable to the address that shows up when you run the server.
- For example, "http://123.0.0.1:5000/"
- Rerun the android app with the updated address.

============================================================================================================================================

Viewing the database table:

The table can be viewed using extensions such as "SQLite Viewer" (for Visual Studio Code).

============================================================================================================================================

Updating the database table:

- Use the command: flask db upgrade (Note: requires Flask-Migrate package)
- See: https://flask-migrate.readthedocs.io/en/latest/

Run the following commands (Note: init is not necessary if the migrations folder exists):

- "flask db init"
- "flask db migrate -m "Initial migration.""
- "flask db upgrade"

============================================================================================================================================

Modifying the database manually:

- Run python first. (Command: "python")

Then, while in python:
- "import sqlite3"
- "conn = sqlite3.connect('login.db')"
- "c = conn.cursor()"

- You can now perform commands using the cursor
- Examples:
- "c.execute("INSERT INTO user VALUES (x, y))"
- "c.execute("INSERT INTO user (username) VALUES ('Test')")"

- When you are done modifying the table, save changes using:
- "conn.commit()"
- Close the connection using:
- "conn.close()"

============================================================================================================================================