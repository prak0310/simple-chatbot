import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="Pr@k031005##",
    database="chatbot_db"
)

print("Connected successfully!")

connection.close()