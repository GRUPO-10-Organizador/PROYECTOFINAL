from datetime import datetime

class Reporte:
    def __init__(self):
        self.__fecha_generacion = datetime.now()

    def generar_resumen(self, portafolio):
        resumen = f"Reporte de Portafolio - {self.__fecha_generacion.strftime('%Y-%m-%d %H:%M:%S')}\n"
        resumen += "-----------------------------------------\n"
        total_valor = 0  # Inicializamos el valor total
        for ticker, cantidad in portafolio.acciones.items():
            accion = portafolio.obtener_accion(ticker)
            valor_accion = accion.precio_actual * cantidad
            total_valor += valor_accion  # Suma al valor total
            resumen += f"{ticker} ({accion.nombre_empresa}): {cantidad} acciones a {accion.precio_actual} cada una (Valor total: {valor_accion})\n"
        resumen += f"Valor Total del Portafolio: {total_valor}\n"
        return resumen

    def guardar_reporte(self, resumen, archivo="reporte.txt"):
        with open(archivo, 'w') as file:
            file.write(resumen)
        print(f"Reporte guardado como {archivo}")

