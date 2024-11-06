class Portafolio:
    def __init__(self, usuario):
        self.__usuario = usuario
        self.__acciones = {}  # Formato: {'accion_id': (accion_obj, cantidad)}

    def agregar_accion(self, accion, cantidad):
        if cantidad > 0:
            if accion.id in self.__acciones:
                # Desempaqueta el objeto de acción y la cantidad actual
                accion_obj, cantidad_existente = self.__acciones[accion.id]
                # Actualiza la cantidad sumando la nueva cantidad
                nueva_cantidad = cantidad_existente + cantidad
                self.__acciones[accion.id] = (accion_obj, nueva_cantidad)
            else:
                # Agrega una nueva entrada con la cantidad inicial
                self.__acciones[accion.id] = (accion, cantidad)
                nueva_cantidad = cantidad  # Nueva cantidad para la base de datos

            # Actualizar en la base de datos
            self.__conexion.actualizar_portafolio(self.__usuario.id, accion.id, nueva_cantidad)
        else:
            raise ValueError("La cantidad debe ser positiva")

    def remover_accion(self, accion, cantidad):
        if accion.id in self.__acciones and cantidad > 0:
            accion_obj, cantidad_existente = self.__acciones[accion.id]
            if cantidad_existente >= cantidad:
                # Actualiza la cantidad restando la cantidad removida
                nueva_cantidad = cantidad_existente - cantidad
                if nueva_cantidad > 0:
                    self.__acciones[accion.id] = (accion_obj, nueva_cantidad)
                else:
                    # Si la cantidad llega a cero, elimina la entrada
                    del self.__acciones[accion.id]
            else:
                raise ValueError("Cantidad insuficiente en portafolio")
        else:
            raise ValueError("Acción no encontrada o cantidad inválida")

    def valor_total(self):
        total = 0
        for _, (accion, cantidad) in self.__acciones.items():
            total += cantidad * accion.precio_actual
        return total

    def mostrar_acciones(self):
        return {accion.id: cantidad for accion, cantidad in self.__acciones.values()}

    def consultar_portafolio(self):
        print(f"Portafolio de {self.__usuario.nombre}:")
        for accion_id, (accion, cantidad) in self.__acciones.items():
            print(f"Acción ID: {accion.id}, Cantidad: {cantidad}, Precio Actual: ${accion.precio_actual:.2f}")
        total_valor = self.valor_total()
        print(f"Valor total del portafolio: ${total_valor:.2f}")

    def __str__(self):
        return f"Portafolio de {self.__usuario.nombre}: {self.mostrar_acciones()}"
