import os
import sqlite3

def get_connection():
    # Obtiene la ruta absoluta de la carpeta actual del proyecto
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'gold_task.db')
    
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection