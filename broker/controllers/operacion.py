from datetime import datetime

class Operacion:
    def __init__(self, usuario_id, accion_id, tipo, cantidad, precio_unitario):
        self.__usuario_id = usuario_id  # ID del usuario
        self.__accion_id = accion_id      # ID de la acción
        self.__tipo = tipo                # Puede ser 'compra' o 'venta'
        self.__cantidad = cantidad
        self.__precio_unitario = precio_unitario
        self.__fecha = datetime.now()

    @property
    def usuario_id(self):
        return self.__usuario_id

    @property
    def accion_id(self):
        return self.__accion_id

    @property
    def tipo(self):
        return self.__tipo

    @property
    def cantidad(self):
        return self.__cantidad

    @property
    def precio_unitario(self):
        return self.__precio_unitario

    @property
    def fecha(self):
        return self.__fecha

    def calcular_total(self):
        return self.__cantidad * self.__precio_unitario

    def validar_operacion(self, manejador_db):
        # Comprobacion si el usuario existe
        if not manejador_db.verificar_usuario_existente(self.__usuario_id):
            raise ValueError("Usuario no existe.")
        
        # 2. Comprobacion si la acción existe
        if not manejador_db.verificar_accion_existente(self.__accion_id):
            raise ValueError("Acción no existe.")
        
        #Comprobar si el usuario tiene suficiente saldo para una compra
        return True  #Retorna True si la operación es válida

    def __str__(self):
        return (f"Operación: {self.__tipo}, Usuario ID: {self.__usuario_id}, "
                f"Acción ID: {self.__accion_id}, Cantidad: {self.__cantidad}, "
                f"Precio Unitario: {self.__precio_unitario}, Fecha: {self.__fecha}")
