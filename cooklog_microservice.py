#  *****    THIS MICROSERVICE WILL BOTH LOG WHEN A RECIPE WAS COOKED AND CAN ALSO RETURN A LOG OF DATES THAT A RECIPE WAS COOKED *****

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from time import sleep

DB_NAME = "otherdatabase.db"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'anythingfarts'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db = SQLAlchemy(app)
app.app_context().push()

from sqlalchemy.sql import func

class Recipe(db.Model):                                                 #  ***** creating a database and backend that I can test
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    logs = db.relationship('Log')

    #create a function to return a string when we add something.
    def __repr__(self):
        return '<name %r>' % self.id
   
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    recipe_id= db.Column(db.Integer, db.ForeignKey('recipe.id'))
    
def addrecipe(recipe_name=None, recipe_category=None, recipe_ingredients=None, recipe_instructions=None):
    thisRecipe = Recipe.query.filter_by(name=recipe_name)
    if thisRecipe.count()>0:
        print('Recipe already exists. Skipping.')
        return 2 # recipe name already exists.
    
    # Else, recipe does not exist so add it.
    new_recipe = Recipe(name=recipe_name, category=recipe_category, ingredients=recipe_ingredients, instructions=recipe_instructions)

    
    try:                                                        
        db.session.add(new_recipe)                                          #  *****  pushing to database
        db.session.commit()
        return 1 # success
    except Exception as e:
        db.session.rollback()
        print(f"Error adding recipe:{str(e)}")
        return 0 # error


def cooklog(recipeName=None, dateLog=None):
    thisRecipe = Recipe.query.filter_by(name=recipeName)
    if thisRecipe.count()<1:
        print('Matching recipe not found')
        logResult = 0

    logRecipe = thisRecipe[0]
    
    if len(dateLog) < 1:
        logResult = 0
    else:
        new_log = Log(data=dateLog, recipe_id=logRecipe.id)                 #  ***** providing the schema for the log 
        db.session.add(new_log)                                             # ***** adding the log to the database 
        db.session.commit()
        logResult = 1

    return logResult

def getcooklog(recipeName):
    thisRecipe = Recipe.query.filter_by(name=recipeName)
    logResult = None
    if thisRecipe.count()<1:
        print('Matching recipe not found')

    logResult = thisRecipe[0]
    #logResult = 1
    return logResult
        
db.create_all()

addrecipe('Cowboy_Pizza','Pizza','Dough, Sauce, Cheese, Meat','Make a pizza and cook it')
addrecipe('Fat_Free_Ramen','Asian Noodles','Top Ramen','Make the ramen. Its fat free!')
cooklog('Fat_Free_Ramen', '01/02/2024')
cooklog('Cowboy_Pizza', '02/02/2024')
cooklog('Fat_Free_Ramen', '03/08/2024')


# ^^^^^  The above is just to create and populate an example database for the microservice to work with ^^^^^

# *****  Now bind to the socket and START the service
import zmq
debug = 1

context = zmq.Context()                                                     #  Connecting to his partner's driver socket
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

#  listen for input in a loop to keep the microservice live
while True:
    message = socket.recv()
    messagestr = str(message)
    if debug == 1:
        print("received message: %s" % messagestr)

    #  clean up input takes out the "b" anomaly
    messagestr = messagestr[2:-1]
    if debug == 1:
        print("input selector is: %s" % messagestr)

    messagestr = messagestr.split()                                         # split the string

    messageIn = messagestr[0]
    if len(messagestr)>1:                                                   #  might not be required anymore?
        
        recipeNameIn = messagestr[1]
    
        if messageIn == "cooklog":                                          #  cooklog is the command for my microservice to add to the log
            recipeLogIn = messagestr[2]
            out = cooklog(recipeNameIn, recipeLogIn)
            if out==0:
                messageOut = "Error"
        # Send error back on socket
            elif out==1:
                messageOut = "Success"
        # Send success back on socket
            socket.send_string(messageOut)

        elif messageIn == "getcooklog":                                     #  getcooklog is the command for my microservice to return the entire log of dates
            print(recipeNameIn)
            recipeLog = getcooklog(recipeNameIn)

            if recipeLog is None:
                messageOut = "Error. Recipe Not Found."
            else:
                messageOut = ""
                for logs in recipeLog.logs:
                    if len(messageOut)<1:
                        messageOut = logs.data
                    else:
                        messageOut = messageOut + ", " + logs.data           #  formatting into one long comma separated string
                    
                print(recipeNameIn+": "+messageOut)
            socket.send_string(messageOut)
