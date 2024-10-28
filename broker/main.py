import mysql
from controllers.manejador_db import ManejadorDB
from models.usuario import Usuario
from models.accion import Accion
from controllers.operacion import Operacion


def mostrar_menu():
    print("\n" + "="*30)
    print("  Bienvenido a ARGBroker Demo  ")
    print("="*30)
    
    # Opciones del menú
    opciones = [
        "1. Registrar nuevo usuario",
        "2. Registrar nueva acción",
        "3. Registrar operación de compra/venta",
        "4. Consultar portafolio de usuario",
        "5. Generar reporte financiero",
        "0. Salir"
    ]
    
    for opcion in opciones:
        print(f"   {opcion}")
    
    print("="*30)


def generar_reporte_financiero(manejador_db, id_usuario):
    # manejador de base de datos
    if not manejador_db.verificar_usuario_existente(id_usuario):
        print("El usuario no existe.")
        return

    # operaciones del usuario
    manejador_db.cursor.execute("SELECT * FROM operacion WHERE usuario_id = %s", (id_usuario,))
    operaciones = manejador_db.cursor.fetchall()

    # construccion de reporte
    print("Reporte Financiero:")
    for operacion in operaciones:
        print(operacion)
    if not operaciones:
        print("No hay operaciones registradas para este usuario.")

def iniciar():
    manejador_db = ManejadorDB(
        host="localhost",
        user="root",
        password="#Naunoplayyt2882",
        database="broker"
    )
    
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            try:
                id_usuario = int(input("Ingrese ID de usuario: "))
                nombre = input("Ingrese nombre de usuario: ")
                email = input("Ingrese email de usuario: ")
                saldo_inicial = float(input("Ingrese saldo inicial: "))

                if manejador_db.verificar_email_existente(email):
                    print(f"El usuario con email {email} ya existe.")
                else:
                    usuario = Usuario(id_usuario, nombre, email, saldo_inicial)
                    manejador_db.guardar_usuario(usuario.id, usuario.nombre, usuario.email, usuario.saldo)

            except ValueError:
                print("Error: Ingrese valores válidos para ID y saldo.")
        
        elif opcion == '2':
            simbolo = input("Ingrese símbolo de la acción (ej: TSLA): ")
            nombre = input("Ingrese nombre de la acción (ej: Tesla): ")

            # Validamos precio actual de la acción
            while True:
                try:
                    precio_actual = float(input("Ingrese precio actual: "))
                    if precio_actual <= 0:
                        print("El precio debe ser un número positivo. Intente de nuevo.")
                        continue
                    break
                except ValueError:
                    print("Entrada inválida. Por favor, ingrese un número válido para el precio.")

            # Validamos que el usuario ingrese un ID de empresa sin permitir campo vacío
            while True:
                empresa_id = input("Ingrese ID de la empresa (no puede estar vacío): ")
                if empresa_id.strip():  # Verifica que no esté vacío
                    if empresa_id.isdigit():
                        empresa_id = int(empresa_id)
                        break
                    else:
                        print("Error: Debe ingresar un número válido para el ID de la empresa.")
                else:
                    print("Error: No se puede dejar el ID de empresa en blanco. Por favor, ingrese un ID.")

            # Verificamos si la empresa existe
            if not manejador_db.verificar_empresa_existente(empresa_id):
                print(f"Error: La empresa con ID '{empresa_id}' no existe.")
                crear_empresa = input("¿Desea crear una nueva empresa con este ID? (s/n): ").lower()
                if crear_empresa == 's':
                    nombre_empresa = input("Ingrese el nombre de la nueva empresa: ")
                    while not nombre_empresa:
                        print("El nombre de la empresa no puede estar vacío.")
                        nombre_empresa = input("Ingrese el nombre de la nueva empresa: ")

                    sector = input("Ingrese el sector de la nueva empresa: ")
                    while not sector:
                        print("El sector de la empresa no puede estar vacío.")
                        sector = input("Ingrese el sector de la nueva empresa: ")

                    pais = input("Ingrese el país de la nueva empresa: ")
                    while not pais:
                        print("El país de la empresa no puede estar vacío.")
                        pais = input("Ingrese el país de la nueva empresa: ")

                    manejador_db.guardar_empresa(nombre_empresa, empresa_id, sector, pais)
                    print(f"Empresa {nombre_empresa} guardada exitosamente con ID {empresa_id}.")
                else:
                    print("Operación cancelada.")
                    continue  # Regresa al menú principal si el usuario no desea crear una nueva empresa

            # Registro de nueva acción
            if manejador_db.verificar_accion_existente(simbolo):
                print(f"Error: La acción con símbolo '{simbolo}' ya existe.")
            else:
                try:
                    # Crear la acción
                    accion = Accion(simbolo=simbolo, nombre=nombre, precio_actual=precio_actual, empresa_id=empresa_id)
                    manejador_db.guardar_accion(accion)
                    print("Acción guardada exitosamente.")
                except Exception as e:
                    print(f"Error al guardar acción: {str(e)}")

        elif opcion == "3":
            try:
                usuario_id = int(input("Ingrese ID de usuario: "))
                if not manejador_db.verificar_usuario_existente(usuario_id):
                    print(f"El usuario con ID {usuario_id} no existe.")
                    continue

                id_accion = int(input("Ingrese ID de la acción: "))
                if not manejador_db.verificar_accion_existente(id_accion):
                    print(f"La acción con ID {id_accion} no existe.")
                    continue

                tipo_operacion = input("Ingrese tipo de operación (compra/venta): ").lower()
                if tipo_operacion not in ["compra", "venta"]:
                    print("Tipo de operación no válida. Debe ser 'compra' o 'venta'.")
                    continue

                cantidad = int(input("Ingrese cantidad de acciones: "))
                if cantidad <= 0:
                    print("La cantidad debe ser mayor a cero.")
                    continue

                precio_unitario = manejador_db.obtener_precio_accion(id_accion)
                operacion = Operacion(usuario_id, id_accion, tipo_operacion, cantidad, precio_unitario)

                if operacion.validar_operacion(manejador_db):
                    manejador_db.guardar_operacion(operacion)
                    print("Operación registrada con éxito.")
                else:
                    print("Operación no válida.")
            except ValueError as ve:
                print(f"Error: {ve}")
            except mysql.connector.Error as db_error:
                print(f"Error de base de datos: {db_error}")
            except Exception as e:
                print(f"Ocurrió un error: {e}")

        elif opcion == '4':
            usuario_id = input("Ingrese ID de usuario para consultar el portafolio: ")
            manejador_db.consultar_portafolio(usuario_id)
                
        elif opcion == "5":
            id_usuario = input("Ingrese ID de usuario para generar el reporte: ")
            generar_reporte_financiero(manejador_db, id_usuario)
        
        elif opcion == "0":
            print("Gracias por usar ARGBroker Demo. ¡Hasta pronto!")
            manejador_db.cerrar_conexion()
            break
        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    iniciar()
