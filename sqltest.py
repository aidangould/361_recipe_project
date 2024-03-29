import pyodbc
server = 'aidan361.database.windows.net'
database = '361RecipeDB'
username = 'azureuser'
password = 'aidan361SQL'
driver= '{ODBC Driver 18 for SQL Server}'

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM [dbo].[recipes]")
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            ##IMPORTANT!! This is only outputting columns 0 and 1!!
            row = cursor.fetchone()