import sqlite3

def crear_base_datos():
    conexion = sqlite3.connect('gold_task.db')
    cursor = conexion.cursor()

    # Tabla de Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Tabla de Categorías
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    ''')

    # Tabla de Tareas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria_id INTEGER,
            fecha_vencimiento TEXT NOT NULL,
            hora TEXT,
            ubicacion TEXT,
            observaciones TEXT,
            prioridad TEXT NOT NULL,
            completada INTEGER DEFAULT 0,
            usuario_id INTEGER,
            FOREIGN KEY (categoria_id) REFERENCES categorias (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    # Insertar categorías por defecto si no existen
    cursor.execute("SELECT COUNT(*) FROM categorias")
    if cursor.fetchone()[0] == 0:
        categorias_iniciales = [
            ('Deporte',), 
            ('Educación',), 
            ('Hogar',), 
            ('Ocio',), 
            ('Otras',), 
            ('Salud',), 
            ('Social',), 
            ('Trabajo',)
        ]   
        cursor.executemany("INSERT INTO categorias (nombre) VALUES (?)", categorias_iniciales)

    conexion.commit()
    conexion.close()
    print("Base de datos SQLite creada e inicializada con éxito.")

if __name__ == '__main__':
    crear_base_datos()