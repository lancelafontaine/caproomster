# SOEN 343 Project - Capstone Room Reservation

This is the repository that contains the code, documentation, issues and much more related to reserving a classroom for a school project.
<br />

<h1>Instructions to setup the environment</h1>
-Checkout and pull master
-Download and install <a href="https://www.python.org/download/releases/2.7/">python2.7</a> version 2.7.12 under the downloads tab<br />
-Follow the instructions at the following <a href="http://flask.pocoo.org/docs/0.11/installation/">link</a> to succesfully download and install Flask</a><br/> 

-pip install the necessary modules mentionned in the requirements text file <br />
<h3>Instruction to install modules</h3>
$ pip install flask flask-security flask-sqlalchemy psycopg2 ... <br />

<h3>Instructions to setup database</h3>
<h6>Directly from their website</h6>
Download and install the latest version of <a href="https://www.postgresql.org/download/">postgresql</a><br />
<h6>Using the terminal for Mac</h6>
install <a href="http://brew.sh/">brew</a>
insert the following command on your terminal: <br />
$ brew install postgresql<br />

-Create a database named development <br />
-Copy the sql script under bookMeDB.sql from the root directory and paste in the query tools <br />
-Change the passwords inside of the TDGs to the password of your postgresql chosen password <br />
-In the config python file insert your password where it says sqlPass<br />

<h2>To start server</h2>
$ python run.py <br />

<h6>The following are the credentials to login:</h6>
 UserId: 1, Username: John, Password:pass <br />
 UserId: 2, Username: Emily, Password:pass <br />
 UserId: 3, Username: Rudy, Password:pass <br />
 UserId: 4, Username: Jackie, Password:pass <br />

## Team Members

Ahmad Hyjaz Loudin - @PuzzlePuzzling<br />
Emir Bozer @emrbzr<br />
Leo Yu @yleo<br />
Nikolas De vigne Blanchet @ndvb <br />
Mary Psaroudis @mary86<br />
