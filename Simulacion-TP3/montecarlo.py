import random

def simular_semana(i, inventario, pedidos_pendientes, params):
    fila = {}

    # verifico si llegó el pedido esta semana
    llegada = [p for p in pedidos_pendientes if p["llega_en"] == i]
    if llegada:
        libros_recibidos = llegada[0]["cantidad"]

        # fallas
        rnd_falla = random.uniform(0, 0.99)
        defectuosos = libros_recibidos * rnd_falla
