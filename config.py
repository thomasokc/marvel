#config is where our enviroment variables live and how flask gets connected to everything

#Allows project to navigate operating system. We can go through the file explorer and mess with things all through the app
import os
from dotenv import load_dotenv

#Takes the absolute path of our file (C drive, user, thoma) and sticks into this var
basedir = os.path.abspath(os.path.dirname(__file__))

#Loads to enviroment
load_dotenv(os.path.join(basedir, '.env'))

#Tells the app where to look to find info, even through our database etc
class Config():
    """
    Set vars in here for the flask app
    """
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')

    #Need for flask to run and prevents cookie tampering
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'CONFIDENTIAL: FOR TOMMY GUNS ONLY'

    #URL's are URI's.. URI's contain URL's
    #Looks for a URL connecting to our database, if not it will store data in SQLAlchemy's local data
    #SQLAchemy translates SQL into readable Python, helping you manage your database with Python
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    #turns off update messages from SQLAchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

