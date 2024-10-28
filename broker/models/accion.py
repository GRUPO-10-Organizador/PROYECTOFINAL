class Accion:
    def __init__(self, simbolo, nombre, precio_actual, empresa_id, id=None):
        self.id = id 
        self.__simbolo = simbolo
        self.__nombre = nombre
        self.precio_actual = precio_actual  # Usamos setter
        self.__empresa_id = empresa_id

    @property
    def simbolo(self):
        return self.__simbolo

    @simbolo.setter
    def simbolo(self, value):
        self.__simbolo = value

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, value):
        self.__nombre = value

    @property
    def precio_actual(self):
        return self.__precio_actual

    @precio_actual.setter
    def precio_actual(self, nuevo_precio):
        if nuevo_precio > 0:
            self.__precio_actual = nuevo_precio
        else:
            raise ValueError("El precio debe ser positivo")

    @property
    def empresa_id(self):
        return self.__empresa_id

    @empresa_id.setter
    def empresa_id(self, value):
        self.__empresa_id = value

    def __str__(self):
        return f"Acción: {self.__simbolo}, Empresa: {self.__nombre}, Precio: {self.__precio_actual}"


