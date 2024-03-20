import time
import zmq

context = zmq.Context()
logSocket = context.socket(zmq.REQ)
logSocket.connect("tcp://localhost:5555")
recipeSocket = context.socket(zmq.REQ)
recipeSocket.connect("tcp://localhost:5556")
introText = "Welcome to the recipe picker! Enter your command below or \"help\" to view available commands or \"exit\" \n\
to exit."
helpText = "These are the available commands. Not sure where to start? Try using \"viewall\" to view all recipes\
 \nYou can also select a recipe by entering the recipe ID number. \
 \nUnless a command requires more input, these can be entered at any time: \
 \n[enter the number of a recipe]:  Views the recipe with the corresponding number \
 \ncookalready:	Find a recipe to cook that only uses ingredients you already have\ncookexpiring:	Find a \
 recipe to cook that uses the ingredient that is expiring soonest\ncooklog:		Log when you cooked a recipe (also \
 updates your inventory)\nexit:			Exits the program\nhelp:			Shows a list of commands\ninventory:		\
 View or update your ingredient inventory\nnotes:		Take notes on a recipe that you have cooked\nshopall:		\
 Outputs a shopping list for all recipes in the database\nshopmissing:	\
 Outputs a shopping list for the ingredients you are missing for one recipe\nviewall:		Shows all the recipes in \
 the app"

recipeInstructionList = ['0', '1', '2', 'viewall']

debug = 1

print(introText)

input1 = input()

while input1 != "exit":
    if debug == 1:
        print(input1)

    if input1 == "help":
        print(helpText)

    elif input1 in recipeInstructionList:
        while True:
            recipeSocket.send_string(input1)
            break

        message = recipeSocket.recv()
        # TO DO: make a message string cleanup method
        messagestr = str(message)
        messagestr = messagestr[2:-1]
        messagestr = messagestr.replace("\\t", "\t")
        messagestr = messagestr.replace("\\n", "\n")
        print(messagestr)
        time.sleep(0.1)  # modification per Jacqueline

    else:
        while True:
            logSocket.send_string(input1)
            break

        message = logSocket.recv()
        messagestr = str(message)
        messagestr = messagestr[2:-1]
        messagestr = messagestr.replace("\\t", "\t")
        messagestr = messagestr.replace("\\n", "\n")
        print(messagestr)
        time.sleep(0.1)  # modification per Jacqueline

    input1 = input()
