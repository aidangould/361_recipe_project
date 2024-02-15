import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
introText = "Welcome to the recipe picker! Enter your command below or \"help\" to view available commands or \"exit\" \n\
to exit."
helpText = "These are the available commands. Not sure where to start? Try using \"viewall\" to view all recipes\
 \nYou can also select a recipe by entering the recipe ID number. \
 \nUnless a command requires more input, these can be entered at any time: \
 \ncookalready:	Find a recipe to cook that only uses ingredients you already have\ncookexpiring:	Find a \
 recipe to cook that uses the ingredient that is expiring soonest\ncooklog:		Log when you cooked a recipe (also \
 updates your inventory)\nexit:			Exits the program\nhelp:			Shows a list of commands\ninventory:		\
 View or update your ingredient inventory\nnotes:		Take notes on a recipe that you have cooked\nrecipe:		\
 View a specific recipe\nshopall:		Outputs a shopping list for all recipes in the database\nshopmissing:	\
 Outputs a shopping list for the ingredients you are missing for one recipe\nviewall:		Shows all the recipes in \
 the app"
debug = 1

print(introText)

input1 = input()

while input1 != "exit":
        if debug == 1:
                print(input1)

        if input1 == "help":
                print(helpText)
        else:
                while True:
                        socket.send_string(input1)
                        break

                message = socket.recv()
                messagestr = str(message)
                messagestr = messagestr[2:-1]
                messagestr = messagestr.replace("\\t", "\t")
                messagestr = messagestr.replace("\\n", "\n")
                print (messagestr)
        input1 = input()