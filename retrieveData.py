import mysql.connector

# Database Info
host = 'frwahxxknm9kwy6c.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
database = 'wtqgvyiyb93cocs8'
username = 'rw7p0k9xiegjz0sh'
password = 'ixdqgdfr7cwqyxss'

#initiate connection between python and MySQL
def connect():
    try:
        connection = mysql.connector.connect(host=host, database=database, user=username, password=password)
        if connection.is_connected():
            return connection
    except Exception as e:
        print("Error while connecting to MySQL database", e)
    return None


# close connection to MySQL database
def close_connection(connection):
    if connection.is_connected():
        connection.close()


# check if user with email and password exist
def check_records(email, connection):
    try:
        find_user = "SELECT * FROM users WHERE email IN ('" +str(email)+"')"
        cursor = connection.cursor()
        cursor.execute(find_user)
        row = cursor.fetchone()
        row_list = list(row)
        cursor.close()
        if len(row_list)!=0:
            return row_list
    except Exception as e:
        print("Error while retrieving user info", e)
    return []


# check if the email and password passed match
def verify_credentials(email, password, connection):
    try:
        find_user = "SELECT * FROM users WHERE email = '"+str(email)+"'"
        cursor = connection.cursor()
        cursor.execute(find_user)
        row = cursor.fetchone()
        row_list = list(row)
        cursor.close()
        if len(row_list)!=0:
            if row_list[1]==password:
                return row_list
    except Exception as e:
        print("Error while retrieving user info", e)
    return []


# Add user data to a database
def add_user(first_name, last_name, email, password, connection):
    try:
        stmt = "INSERT INTO users VALUES (%s, %s, %s, %s)"
        val = (str(email), str(password), str(first_name), str(last_name))
        cursor = connection.cursor()
        cursor.execute(stmt, val)
        connection.commit()
        cursor.close()
    except Exception as e:
        print("Failed to enter in user", e)


# obtain all files for a user
def get_images(email, connection):
    user_images = []
    try:
        stmt = "SELECT * FROM images WHERE email = '"+str(email)+"'"
        cursor = connection.cursor()
        cursor.execute(stmt)
        results = cursor.fetchall()
        results_list = list(results)
        for record in results_list:
            user_images.append(record)
        cursor.close()
    except Exception as e:
        print("Error retrieving user images: ", e)
    return user_images


#add images to personal database
def add_images(image_title, image_reference, email, connection):
    try:
        stmt = "INSERT INTO images VALUES (%s, %s, %s)"
        val = (str(image_title), str(image_reference), email)
        cursor = connection.cursor()
        cursor.execute(stmt, val)
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print("error adding image:", e)
    return False


# remove images
def remove_images(image_title, image_ref, email, connection):
    try:
        stmt = "DELETE FROM images WHERE image_title = %s AND image_ref = %s AND email = %s"
        val = (str(image_title), str(image_ref), str(email))    
        cursor = connection.cursor()
        cursor.execute(stmt, val)
        connection.commit()
        cursor.close()
    except Exception as e:
        print("Error removing query:", e)
