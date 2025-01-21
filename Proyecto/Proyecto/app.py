from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'atlas_database'
}

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['user']
        contraseña = request.form['code']
        action = request.form['action']

        if not usuario or not contraseña:
            return jsonify({'success': False, 'message': 'Usuario y Contraseña no pueden estar vacíos'})

        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                cursor = conn.cursor()

                if action == 'login':
                    cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND contraseña=%s", (usuario, contraseña))
                    result = cursor.fetchone()
                    
                    if result:
                        session['usuario'] = usuario
                        return jsonify({'success': True})
                    else:
                        return jsonify({'success': False, 'message': 'Usuario o Contraseña incorrectos'})
                
                elif action == 'register':
                    cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario,))
                    result = cursor.fetchone()
                    
                    if result:
                        return jsonify({'success': False, 'message': 'El usuario ya está registrado'})
                    else:
                        cursor.execute("INSERT INTO usuarios (usuario, contraseña) VALUES (%s, %s)", (usuario, contraseña))
                        conn.commit()
                        return jsonify({'success': True, 'message': 'Usuario registrado exitosamente'})

                cursor.close()
                conn.close()
            else:
                return jsonify({'success': False, 'message': 'No se pudo conectar a la base de datos'})
        except Error as err:
            return jsonify({'success': False, 'message': f'Error al conectar a la base de datos: {err}'})

    return render_template('index.html')

@app.route('/inventory')
def inventory():
    if 'usuario' in session:
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                cursor = conn.cursor()
                
                # Obtener el usuario_id del usuario en sesión
                cursor.execute("SELECT usuario_id FROM usuarios WHERE usuario=%s", (session['usuario'],))
                user_id = cursor.fetchone()[0]  # Obtener el ID del usuario
                
                # Obtener solo los productos del usuario
                cursor.execute("SELECT * FROM productos WHERE user_id = %s", (user_id,))
                productos = cursor.fetchall()
                total_inventario = sum(producto[3] * producto[4] for producto in productos)
                
                cursor.close()
                conn.close()
            else:
                productos = []
                total_inventario = 0
        except Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            productos = []
            total_inventario = 0
        
        return render_template('inventory.html', usuario=session['usuario'], productos=productos, total_inventario=total_inventario)
    else:
        return redirect(url_for('login'))

@app.route('/registrar_producto')
def registrar_producto():
    if 'usuario' in session:
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                cursor = conn.cursor()
                
                # Obtener el usuario_id del usuario en sesión
                cursor.execute("SELECT usuario_id FROM usuarios WHERE usuario=%s", (session['usuario'],))
                user_id = cursor.fetchone()[0]  # Obtener el ID del usuario
                
                # Obtener todas las categorías del usuario
                cursor.execute("SELECT * FROM categorias WHERE user_id = %s", (user_id,))
                categorias = cursor.fetchall()
                
                cursor.close()
                conn.close()
                
                return render_template('registrar_producto.html', categorias=categorias)
            else:
                return redirect(url_for('login'))
        except Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/save_product', methods=['POST'])
def save_product():
    if 'usuario' in session:
        product_name = request.form['product_name']
        unit_price = request.form['unit_price'] 
        unit_buy = request.form['unit_buy']
        quantity = request.form['quantity']
        categoria_id = request.form['categoria']  # Cambiado a categoria_id
        
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                cursor = conn.cursor()
                
                # Obtener el usuario_id del usuario en sesión
                cursor.execute("SELECT usuario_id FROM usuarios WHERE usuario=%s", (session['usuario'],))
                user_id = cursor.fetchone()[0]  # Obtener el ID del usuario
                
                # Insertar el producto con el user_id
                cursor.execute("INSERT INTO productos (nombre, costo,precio_unitario, cantidad, categoria, user_id) VALUES (%s, %s, %s, %s, %s, %s)", 
                               (product_name, unit_price, unit_buy, quantity, categoria_id, user_id))
                conn.commit()
                cursor.close()
                conn.close()
        except Error as err:
            print(f"Error al conectar a la base de datos: {err}")
        
        return redirect(url_for('inventory'))
    else:
        return redirect(url_for('login'))

@app.route('/wallet')
def wallet():
    if 'usuario' in session:
        return render_template('wallet.html')
    else:
        return redirect(url_for('login'))

@app.route('/empleados')
def empleados():
    if 'usuario' in session:
        return render_template('empleados.html')
    else:
        return redirect(url_for('login'))

@app.route('/proveedores')
def proveedores():
    if 'usuario' in session:
        return render_template('proveedores.html')
    else:
        return redirect(url_for('login'))

@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    if 'usuario' in session:
        if request.method == 'POST':
            # Crear nueva categoría
            categoria_nombre = request.form['categoria_nombre']
            try:
                conn = mysql.connector.connect(**db_config)
                if conn.is_connected():
                    cursor = conn.cursor()
                    # Obtener el usuario_id del usuario en sesión
                    cursor.execute("SELECT usuario_id FROM usuarios WHERE usuario=%s", (session['usuario'],))
                    user_id = cursor.fetchone()[0]  # Obtener el ID del usuario
                    
                    # Insertar la nueva categoría
                    cursor.execute("INSERT INTO categorias (nombre, user_id) VALUES (%s, %s)", (categoria_nombre, user_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return redirect(url_for('categorias'))
            except Error as err:
                print(f"Error al conectar a la base de datos: {err}")
        else:
            # Listar categorías
            try:
                conn = mysql.connector.connect(**db_config)
                if conn.is_connected():
                    cursor = conn.cursor()
                    # Obtener el usuario_id del usuario en sesión
                    cursor.execute("SELECT usuario_id FROM usuarios WHERE usuario=%s", (session['usuario'],))
                    user_id = cursor.fetchone()[0]  # Obtener el ID del usuario
                    
                    # Obtener todas las categorías del usuario
                    cursor.execute("SELECT * FROM categorias WHERE user_id = %s", (user_id,))
                    categorias = cursor.fetchall()
                    cursor.close()
                    conn.close()
                else:
                    categorias = []
            except Error as err:
                print(f"Error al conectar a la base de datos: {err}")
                categorias = []
        
        return render_template('categorias.html', categorias=categorias)
    else:
        return redirect(url_for('login'))

@app.route('/test', methods=['GET'])
def test():
    if 'usuario' in session:
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                cursor = conn.cursor()
                
                # Obtener el usuario_id del usuario en sesión
                cursor.execute("SELECT usuario_id FROM usuarios WHERE usuario=%s", (session['usuario'],))
                user_id = cursor.fetchone()[0]  # Obtener el ID del usuario
                
                # Filtrar productos por categoría si se proporciona
                categoria_id = request.args.get('categoria_id')
                if categoria_id:
                    cursor.execute("SELECT * FROM productos WHERE user_id = %s AND categoria = %s", (user_id, categoria_id))
                else:
                    cursor.execute("SELECT * FROM productos WHERE user_id = %s", (user_id,))
                
                productos = cursor.fetchall()
                cursor.close()
                conn.close()
            else:
                productos = []
        except Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            productos = []
        
        # Obtener todas las categorías para el filtro
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM categorias WHERE user_id = %s", (user_id,))
                categorias = cursor.fetchall()
                cursor.close()
                conn.close()
            else:
                categorias = []
        except Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            categorias = []
        
        return render_template('productos.html', usuario=session['usuario'], productos=productos, categorias=categorias)
    else:
        return redirect(url_for('login'))
    
@app.route('/productos', methods=['GET', 'POST'])
def productos():
    if 'usuario' in session:
        productos = []
        categorias = []
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                cursor = conn.cursor()
                
                # Obtener el usuario_id del usuario en sesión
                cursor.execute("SELECT usuario_id FROM usuarios WHERE usuario=%s", (session['usuario'],))
                user_id = cursor.fetchone()[0]  # Obtener el ID del usuario
                
                # Obtener la categoría del formulario, si existe
                categoria = request.args.get('categoria')  # Usamos GET para obtener el parámetro de la URL
                
                # Construir la consulta SQL
                if categoria:
                    cursor.execute("SELECT * FROM productos WHERE user_id = %s AND categoria = %s", (user_id, categoria))
                else:
                    cursor.execute("SELECT * FROM productos WHERE user_id = %s", (user_id,))
                
                productos = cursor.fetchall()
                
                # Obtener las categorías disponibles para el filtro
                cursor.execute("SELECT DISTINCT categoria FROM productos WHERE user_id = %s", (user_id,))
                categorias = cursor.fetchall()
                
                cursor.close()
                conn.close()
            else:
                productos = []
        except Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            productos = []
        
        return render_template('productos.html', usuario=session['usuario'], productos=productos, categorias=categorias, categoria=categoria)
    else:
        return redirect(url_for('login'))


@app.route('/historial_ventas')
def historial_ventas():
    if 'usuario' in session:
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                cursor = conn.cursor()
                
                # Obtener el usuario_id del usuario en sesión
                cursor.execute("SELECT usuario_id FROM usuarios WHERE usuario=%s", (session['usuario'],))
                user_id = cursor.fetchone()[0]  # Obtener el ID del usuario
                
                # Obtener historial de ventas del usuario
                cursor.execute("SELECT * FROM ventas WHERE user_id = %s", (user_id,))
                ventas = cursor.fetchall()
                cursor.close()
                conn.close()
    
            else:
                ventas = []
        except Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            ventas = []
        
        return render_template('historial_ventas.html', usuario=session['usuario'], ventas=ventas)
    else:
        return redirect(url_for('login'))
@app.route('/realizar_venta', methods=['GET', 'POST'])
def realizar_venta():
    if 'usuario' in session:
        if request.method == 'POST':
            try:
                conn = mysql.connector.connect(**db_config)
                if conn.is_connected():
                    cursor = conn.cursor()

                    # Obtener el usuario_id del usuario en sesión
                    cursor.execute("SELECT usuario_id FROM usuarios WHERE usuario=%s", (session['usuario'],))
                    user_id = cursor.fetchone()[0]  # Obtener el ID del usuario
                
                    # Obtener solo los productos del usuario
                    cursor.execute("SELECT * FROM productos WHERE user_id = %s", (user_id,))
                    productos = cursor.fetchall()

                    for producto in productos:
                        producto_id = producto[0]  # ID del producto
                        cantidad_a_vender = request.form.get(f'cantidad_{producto_id}', 0, type=int)
                        
                        if cantidad_a_vender > 0:
                            # Obtener el nombre y precio del producto
                            nombre_producto = producto[1]
                            precio_unitario = producto[4]
                            precio_total = cantidad_a_vender * precio_unitario

                            # Insertar la venta en la tabla de ventas
                            cursor.execute("INSERT INTO ventas (nombre_producto, cantidad_vendida, precio_total, user_id) VALUES (%s, %s, %s, %s)",
                                           (nombre_producto, cantidad_a_vender, precio_total, user_id))
                            
                            # Actualizar la cantidad del producto en la tabla de productos
                            nueva_cantidad = producto[3] - cantidad_a_vender
                            cursor.execute("UPDATE productos SET cantidad = %s WHERE id = %s", (nueva_cantidad, producto_id))
                    
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return redirect(url_for('historial_ventas'))  # Redirigir a la página de ventas
                else:
                    return jsonify({'success': False, 'message': 'No se pudo conectar a la base de datos'})
            except Error as err:
                print(f"Error al conectar a la base de datos: {err}")
                return jsonify({'success': False, 'message': f'Error: {err}'})
        else:
            try:
                conn = mysql.connector.connect(**db_config)
                if conn.is_connected():
                    cursor = conn.cursor()
                    
                    # Obtener el usuario_id del usuario en sesión
                    cursor.execute("SELECT usuario_id FROM usuarios WHERE usuario=%s", (session['usuario'],))
                    user_id = cursor.fetchone()[0]  # Obtener el ID del usuario
                    
                    # Obtener solo los productos del usuario
                    cursor.execute("SELECT * FROM productos WHERE user_id = %s", (user_id,))
                    productos = cursor.fetchall()
                    cursor.close()
                    conn.close()
                else:
                    productos = []
            except Error as err:
                print(f"Error al conectar a la base de datos: {err}")
                productos = []
            return render_template('realizar_venta.html', productos=productos)
    else:
        return redirect(url_for('login'))

from datetime import datetime

from datetime import datetime, timedelta

@app.route('/ganancias')
def ganancias():
    if 'usuario' in session:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Convertir las fechas a formato datetime si están presentes
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            # Añadir un día a end_date para incluir todo el día seleccionado
            end_date += timedelta(days=1)

        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                cursor = conn.cursor()

                # Obtener el usuario_id del usuario en sesión
                cursor.execute("SELECT usuario_id FROM usuarios WHERE usuario=%s", (session['usuario'],))
                user_id = cursor.fetchone()[0]  # Obtener el ID del usuario

                # Construir la consulta SQL con los filtros de fechas si están presentes
                if start_date and end_date:
                    query = """
                        SELECT precio_total, cantidad_vendida, nombre_producto, fecha 
                        FROM ventas 
                        WHERE user_id = %s AND fecha BETWEEN %s AND %s
                    """
                    cursor.execute(query, (user_id, start_date, end_date))
                else:
                    query = """
                        SELECT precio_total, cantidad_vendida, nombre_producto, fecha 
                        FROM ventas 
                        WHERE user_id = %s
                    """
                    cursor.execute(query, (user_id,))

                ventas = cursor.fetchall()

                # Calcular las ganancias totales
                total_ganancias = sum(venta[0] for venta in ventas)

                # Obtener el costo total de los productos vendidos y crear una lista detallada
                total_costos = 0
                detalles_ventas = []
                for venta in ventas:
                    nombre_producto = venta[2]
                    cantidad_vendida = venta[1]

                    # Obtener el costo del producto
                    cursor.execute("SELECT costo FROM productos WHERE nombre = %s AND user_id = %s", (nombre_producto, user_id))
                    costo_producto = cursor.fetchone()
                    if costo_producto:
                        costo_total_producto = costo_producto[0] * cantidad_vendida
                        total_costos += costo_total_producto

                        # Añadir detalles de la venta a la lista, formateando la fecha
                        detalles_ventas.append({
                            'nombre_producto': nombre_producto,
                            'cantidad_vendida': cantidad_vendida,
                            'precio_total': venta[0],
                            'costo_total_producto': costo_total_producto,
                            'ganancia_bruta': venta[0] - costo_total_producto,
                            'fecha_venta': venta[3].strftime("%Y-%m-%d %H:%M:%S")  # Formatear la fecha aquí
                        })

                # Calcular las ganancias netas
                ganancias_brutas = total_ganancias - total_costos

                cursor.close()
                conn.close()

            else:
                ganancias_brutas = 0
                detalles_ventas = []
        except Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            ganancias_netas = 0
            detalles_ventas = []

        # Asegurarse de que end_date no sea None antes de restar timedelta
        if start_date and end_date:
            end_date -= timedelta(days=1)

        return render_template('ganancias.html', usuario=session['usuario'], ganancias=ganancias_brutas, detalles_ventas=detalles_ventas, start_date=start_date, end_date=end_date)
    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)