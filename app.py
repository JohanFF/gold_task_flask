from flask import Flask, render_template, request, redirect, url_for, session
from config import get_connection

app = Flask(__name__)
app.secret_key = 'gold_task_secret_key_temporal'  # Clave necesaria para manejar la sesión del usuario

# 1. Página de inicio (Landing Page)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Vista y lógica de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        connection.close()
        
        # Validación de credenciales
        if usuario and usuario['password'] == password:
            session['usuario_id'] = usuario['id']
            session['nombre'] = usuario['nombre']
            return redirect(url_for('dashboard'))
        else:
            error = "Correo o contraseña incorrectos."
            
    return render_template('login.html', error=error)

# 3. Vista y lógica de Registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        
        try:
            connection = get_connection()
            cursor = connection.cursor()
            
            # Verificamos si el correo ya está registrado
            cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
            existe = cursor.fetchone()
            
            if existe:
                cursor.close()
                connection.close()
                return "Este correo ya está registrado. <a href='/registro'>Intentar con otro</a>"
            
            # Insertamos el nuevo usuario
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)",
                (nombre, email, password)
            )
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('login'))
        except Exception as e:
            return f"Error en la base de datos al registrar: {e}. <a href='/registro'>Volver</a>"
        
    return render_template('registro.html')

# 4. Panel Principal (Dashboard con categorías y tareas)
@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    usuario_id = session['usuario_id']
    categoria_filtro = request.args.get('categoria_id', type=int)
    
    connection = get_connection()
    cursor = connection.cursor()
    
    # Obtener todas las categorías para los botones de filtro
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    
    # Obtener tareas filtradas por usuario y categoría (si aplica)
    if categoria_filtro:
        cursor.execute(
            "SELECT * FROM tareas WHERE usuario_id = ? AND categoria_id = ?",
            (usuario_id, categoria_filtro)
        )
    else:
        cursor.execute(
            "SELECT * FROM tareas WHERE usuario_id = ?",
            (usuario_id,)
        )
    tareas = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('dashboard.html', tareas=tareas, categorias=categorias, categoria_filtro=categoria_filtro)

# 5. Crear Nueva Tarea
@app.route('/tareas/crear', methods=['GET', 'POST'])
def crear_tarea():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    connection = get_connection()
    if request.method == 'POST':
        titulo = request.form['titulo']
        categoria_id = request.form['categoria_id']
        fecha_vencimiento = request.form['fecha_vencimiento']
        hora = request.form.get('hora') or None
        ubicacion = request.form.get('ubicacion') or None
        observaciones = request.form.get('observaciones') or None
        prioridad = request.form['prioridad']
        usuario_id = session['usuario_id']
        
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO tareas (titulo, categoria_id, fecha_vencimiento, hora, ubicacion, observaciones, prioridad, usuario_id) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (titulo, categoria_id, fecha_vencimiento, hora, ubicacion, observaciones, prioridad, usuario_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('dashboard'))
        
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('crear_tarea.html', categorias=categorias)

# 6. Marcar Tarea como Completada
@app.route('/tareas/completar/<int:id>')
def completar_tarea(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE tareas SET completada = 1 WHERE id = ?", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('dashboard'))

# 7. Eliminar Tarea
@app.route('/tareas/eliminar/<int:id>')
def eliminar_tarea(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = ?", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('dashboard'))

# 8. Formulario para Editar Tarea (GET) y Guardar Cambios (POST)
@app.route('/tareas/editar/<int:id>', methods=['GET', 'POST'])
def editar_tarea(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    connection = get_connection()
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        categoria_id = request.form['categoria_id']
        fecha_vencimiento = request.form['fecha_vencimiento']
        hora = request.form.get('hora') or None
        ubicacion = request.form.get('ubicacion') or None
        observaciones = request.form.get('observaciones') or None
        prioridad = request.form['prioridad']
        
        cursor = connection.cursor()
        cursor.execute(
            """UPDATE tareas SET titulo = ?, categoria_id = ?, fecha_vencimiento = ?, 
                hora = ?, ubicacion = ?, observaciones = ?, prioridad = ? 
                WHERE id = ?""",
            (titulo, categoria_id, fecha_vencimiento, hora, ubicacion, observaciones, prioridad, id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('dashboard'))
        
    # Método GET: Cargar la tarea existente y las categorías
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tareas WHERE id = ?", (id,))
    tarea = cursor.fetchone()
    
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    cursor.close()
    connection.close()
    
    if not tarea:
        return "Tarea no encontrada. <a href='/dashboard'>Volver al panel</a>"
        
    return render_template('editar_tarea.html', tarea=tarea, categorias=categorias)

# 9. Cerrar Sesión (Logout)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)