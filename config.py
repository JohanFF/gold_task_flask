import sqlite3

def get_connection():
    # Esto creará un archivo llamado 'gold_task.db' automáticamente en la carpeta de tu proyecto
    connection = sqlite3.connect('gold_task.db')
    # Permite acceder a las columnas por nombre (como diccionarios, igual que fetchone() de pymysql)
    connection.row_factory = sqlite3.Row
    return connection