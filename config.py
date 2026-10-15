import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        port=3307,          # Puerto actualizado a 3307
        user='root',
        password='',
        database='gold_task_db', # Nombre exacto de tu base de datos
        cursorclass=pymysql.cursors.DictCursor
    )