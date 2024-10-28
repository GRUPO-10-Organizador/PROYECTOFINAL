class Usuario:
    def __init__(self, id_usuario=None, nombre=None, email=None, saldo_inicial=0):
        self.__id = id_usuario  # La ID puede ser None si no se proporciona
        self.__email = email
        self.__nombre = nombre
        self.__saldo = saldo_inicial
        self.__portafolio = {}

    @property
    def id(self):
        return self.__id

    @property
    def email(self):
        return self.__email


    @property
    def nombre(self):
        return self.__nombre

    @property
    def saldo(self):
        return self.__saldo

    @id.setter
    def id(self, id):
        self.__id = id  # Método para establecer el ID

    @saldo.setter
    def saldo(self, nuevo_saldo):
        if nuevo_saldo >= 0:
            self.__saldo = nuevo_saldo
        else:
            raise ValueError("El saldo no puede ser negativo")

    def agregar_accion(self, accion, cantidad):
        if cantidad > 0:
            if accion.ticker in self.__portafolio:
                self.__portafolio[accion.ticker] += cantidad
            else:
                self.__portafolio[accion.ticker] = cantidad
        else:
            raise ValueError("La cantidad debe ser positiva")

    def remover_accion(self, accion, cantidad):
        if accion.ticker in self.__portafolio and cantidad > 0:
            if self.__portafolio[accion.ticker] >= cantidad:
                self.__portafolio[accion.ticker] -= cantidad
                if self.__portafolio[accion.ticker] == 0:
                    del self.__portafolio[accion.ticker]
            else:
                raise ValueError("Cantidad insuficiente en portafolio")
        else:
            raise ValueError("Acción no encontrada en portafolio o cantidad no válida")

    def mostrar_portafolio(self):
        for ticker, cantidad in self.__portafolio.items():
            print(f"{ticker}: {cantidad} acciones")

    def __str__(self):
        return f"Usuario: {self.__nombre}, Saldo: {self.__saldo}, Portafolio: {self.__portafolio}"

