import retrieveData

conn = retrieveData.connect()
retrieveData.remove_images("KDA_Akali", "KDA_Akali.jpg", "ethan.ye0312@gmail.com", conn)
retrieveData.close_connection(conn)