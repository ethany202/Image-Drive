import mysql.connector

host = 'frwahxxknm9kwy6c.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
database = 'wtqgvyiyb93cocs8'
username = 'rw7p0k9xiegjz0sh'
password = 'ixdqgdfr7cwqyxss'

try:
    connection = mysql.connector.connect(host=host, database=database, user=username, password=password)
    if connection.is_connected():
        print("Connecteds")
    db_info = connection.get_server_info()
    print(db_info)


except Exception as e:
    print("Error while connecting to MySQL database", e)
finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")


print("Hello World")

# Select query for user
# email = "alksjlkasjd@hotmail.com" # temporary email
# select_user = "SELECT * FROM users WHERE email in (" + str(email)+")"
# print(select_user)
# cursor = connection.cursor()
# cursor.execute(select_user)
# row = cursor.fetchone()