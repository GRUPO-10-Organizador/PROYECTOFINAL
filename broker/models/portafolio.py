class Portafolio:
    def __init__(self, usuario):
        self.__usuario = usuario
        self.__acciones = {}  # Formato: {'ticker': (accion_obj, cantidad)}

    def agregar_accion(self, accion, cantidad):
        if cantidad > 0:
            if accion.ticker in self.__acciones:
                self.__acciones[accion.ticker][1] += cantidad
            else:
                self.__acciones[accion.ticker] = [accion, cantidad]
        else:
            raise ValueError("La cantidad debe ser positiva")

    def remover_accion(self, accion, cantidad):
        if accion.ticker in self.__acciones and cantidad > 0:
            if self.__acciones[accion.ticker][1] >= cantidad:
                self.__acciones[accion.ticker][1] -= cantidad
                if self.__acciones[accion.ticker][1] == 0:
                    del self.__acciones[accion.ticker]
            else:
                raise ValueError("Cantidad insuficiente en portafolio")
        else:
            raise ValueError("Acción no encontrada o cantidad inválida")

    def valor_total(self):
        total = 0
        for ticker, (accion, cantidad) in self.__acciones.items():
            total += cantidad * accion.precio_actual
        return total

    def mostrar_acciones(self):
        return {ticker: cantidad for ticker, (accion, cantidad) in self.__acciones.items()}

    def consultar_portafolio(self):
        print(f"Portafolio de {self.__usuario.nombre}:")
        for ticker, (accion, cantidad) in self.__acciones.items():
            print(f"{ticker}: {cantidad} acciones a ${accion.precio_actual:.2f} cada una")
        total_valor = self.valor_total()
        print(f"Valor total del portafolio: ${total_valor:.2f}")

    def __str__(self):
        return f"Portafolio de {self.__usuario.nombre}: {self.mostrar_acciones()}"
