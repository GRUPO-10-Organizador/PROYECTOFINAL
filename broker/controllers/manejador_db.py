import mysql.connector
from models.usuario import Usuario

class ManejadorDB:
    def __init__(self, host, user, password, database):
        self.conexion = self.conectar_a_base_datos(host, user, password, database)
        self.cursor = self.conexion.cursor()

    def conectar_a_base_datos(self, host, user, password, database):
        try:
            conexion = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("Conexión exitosa a la base de datos.")
            return conexion
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return None

    def verificar_email_existente(self, email):
        self.cursor.execute("SELECT COUNT(*) FROM usuario WHERE email = %s", (email,))
        resultado = self.cursor.fetchone()
        return resultado[0] > 0

    def verificar_usuario_existente(self, id_usuario):
        self.cursor.execute("SELECT COUNT(*) FROM usuario WHERE id = %s", (id_usuario,))
        resultado = self.cursor.fetchone()
        return resultado[0] > 0

    def verificar_accion_existente(self, id_accion):
        self.cursor.execute("SELECT COUNT(*) FROM accion WHERE id = %s", (id_accion,))
        resultado = self.cursor.fetchone()
        return resultado[0] > 0

    def guardar_usuario(self, id_usuario, nombre, email, saldo_inicial):
        try:
            self.cursor.execute(
                "INSERT INTO usuario (id, nombre, email, saldo) VALUES (%s, %s, %s, %s)",
                (id_usuario, nombre, email, saldo_inicial)
            )
            self.conexion.commit()
            print(f"Usuario {nombre} guardado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def guardar_accion(self, accion):
        if self.verificar_accion_existente(accion.simbolo):
            print(f"Error: La acción con símbolo '{accion.simbolo}' ya existe.")
            return

        query = "INSERT INTO accion (id, simbolo, nombre, precio_actual, empresa_id) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (accion.id, accion.simbolo, accion.nombre, accion.precio_actual, accion.empresa_id))
        self.conexion.commit()

    def guardar_operacion(self, operacion):
        query = ("INSERT INTO operacion (usuario_id, accion_id, tipo, cantidad, precio_unitario) "
                 "VALUES (%s, %s, %s, %s, %s)")
        self.cursor.execute(query, (operacion.usuario_id, operacion.accion_id, operacion.tipo, operacion.cantidad, operacion.precio_unitario))
        self.conexion.commit()
        # Actualizar el portafolio del usuario
        self.actualizar_portafolio(operacion)

    def actualizar_portafolio(self, operacion):
        # Obtener la cantidad actual de la acción en el portafolio del usuario
        self.cursor.execute("SELECT cantidad FROM Portafolio WHERE usuario_id = %s AND accion_id = %s", (operacion.usuario_id, operacion.accion_id))
        resultado = self.cursor.fetchone()
        
        cantidad_actual = resultado[0] if resultado else 0
        # Calcular la nueva cantidad
        if operacion.tipo == "compra":
            nueva_cantidad = cantidad_actual + operacion.cantidad
        elif operacion.tipo == "venta":
            nueva_cantidad = cantidad_actual - operacion.cantidad

        # Validar que la cantidad no sea negativa
        if nueva_cantidad < 0:
            raise ValueError("Operación no válida: el usuario no tiene suficientes acciones para vender.")

        # Insertar o actualizar el registro en `Portafolio`
        if resultado:
            # Actualizar si la acción ya está en el portafolio del usuario
            self.cursor.execute("UPDATE Portafolio SET cantidad = %s WHERE usuario_id = %s AND accion_id = %s", (nueva_cantidad, operacion.usuario_id, operacion.accion_id))
        else:
            # Insertar si es una nueva acción en el portafolio del usuario
            self.cursor.execute("INSERT INTO Portafolio (usuario_id, accion_id, cantidad) VALUES (%s, %s, %s)", (operacion.usuario_id, operacion.accion_id, nueva_cantidad))

        self.conexion.commit()

    def obtener_precio_accion(self, id_accion):
        self.cursor.execute("SELECT precio_actual FROM accion WHERE id = %s", (id_accion,))
        resultado = self.cursor.fetchone()
        if resultado:
            return float(resultado[0])
        else:
            raise ValueError("Acción no encontrada")

    def obtener_usuario(self, usuario_id):
        self.cursor.execute("SELECT * FROM usuario WHERE id = %s", (usuario_id,))
        resultado = self.cursor.fetchone()
    
        if resultado:
            return Usuario(id_usuario=resultado[0], nombre=resultado[1], email=resultado[2], saldo_inicial=resultado[3])
        else:
            raise ValueError("Usuario no encontrado")

    def verificar_empresa_existente(self, empresa_id):
        self.cursor.execute("SELECT COUNT(*) FROM empresa WHERE id = %s", (empresa_id,))
        resultado = self.cursor.fetchone()
        return resultado[0] > 0

    def guardar_empresa(self, nombre_empresa, empresa_id, sector, pais):
        try:
            query = "INSERT INTO empresa (id, nombre, sector, pais) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (empresa_id, nombre_empresa, sector, pais))
            self.conexion.commit()
            print("Empresa registrada exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al guardar la empresa: {err}")

    def consultar_portafolio(self, usuario_id):
        if not self.verificar_usuario_existente(usuario_id):
            print("El usuario no existe.")
            return

        portafolio = self.obtener_portafolio(usuario_id)
        if not portafolio:
            print("El portafolio está vacío.")
            return

        print(f"Portafolio para el usuario ID {usuario_id}:")
        for accion_id, cantidad in portafolio:
            print(f"Acción ID: {accion_id}, Cantidad: {cantidad}")
        return

    def obtener_portafolio(self, usuario_id):
        try:
            self.cursor.execute("SELECT accion_id, cantidad FROM Portafolio WHERE usuario_id = %s", (usuario_id,))
            resultado = self.cursor.fetchall()
            print("Resultado de la consulta:", resultado)
            return resultado
        except Exception as e:
            print("Error al obtener el portafolio:", e)
            return []

    def cerrar_conexion(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
