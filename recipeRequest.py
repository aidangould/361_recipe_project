import pyodbc
import zmq
server = 'aidan361.database.windows.net'
database = '361RecipeDB'
username = 'azureuser'
password = 'aidan361SQL'
driver= '{ODBC Driver 18 for SQL Server}'
debug = 1

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

#listen for input
while True:
    if debug == 1:
        print("starting loop")
    message = socket.recv()
    messagestr = str(message)
    if debug == 1:
        print("received message: %s" % messagestr)


    #clean up input
    messagestr = messagestr[2:-1]
    if debug == 1:
        print("input selector is: %s" % messagestr)

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            #view all recipes
            if messagestr == "viewall":
                cursor.execute("SELECT * FROM [dbo].[recipes]")
                row = cursor.fetchone()
                recipe_string = ""
                while row:
                    if debug == 1:
                        print (str(row[0]) + " " + str(row[1]))
                        ##IMPORTANT!! This is only outputting columns 0 and 1!!
                    recipe_string = "{0}ID: {1}\tname: {2}\n".format(recipe_string, str(row[0]), str(row[19]))

                    row = cursor.fetchone()
                socket.send_string(recipe_string)

            #get recipe by recipe ID
            else:
                cursor.execute("SELECT * FROM [dbo].[recipes] WHERE RecipeID={}".format(messagestr))
                row = cursor.fetchone()
                while row:
                    if debug == 1:
                        print (str(row[0]) + " " + str(row[1]))
                        ##IMPORTANT!! This is only outputting columns 0 and 1!!
                    recipe_string = ""
                    for i in range (len(row)):
                        recipe_string = recipe_string +" " + str(row[i])
                    socket.send_string(recipe_string)
                    row = cursor.fetchone()


            #find recipes by ingredient

        #etc.