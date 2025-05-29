import random

# ----------------------------- UTILIDADES ----------------------------- #
def generar_variable_discreta(rnd, valores, probabilidades):
    acumulada = 0
    for valor, prob in zip(valores, probabilidades):
        acumulada += prob
        if rnd < acumulada:
            return valor
    return valores[-1]

# ------------------------ FUNCIÓN DE SIMULACIÓN ----------------------- #
def simular_semana(semana, estado, config):
    inventario = estado["inventario"]
    pedido_en_camino = estado["pedido_en_camino"]
    tiempo_entrega = estado["tiempo_entrega"]
    llegada_prevista = estado.get("llegada_prevista", None)

    llegada_pedido = False
    cantidad_recibida = 0
    costo_pedido = 0
    rnd_defec = None
    rnd_tiempo = None
    tiempo_estimado = None

    # 1. Llega pedido si corresponde
    if pedido_en_camino:
        estado["tiempo_entrega"] -= 1
        if estado["tiempo_entrega"] == 0:
            llegada_pedido = True
            rnd_defec = random.random()
            cantidad_recibida = sum(random.random() >= config["prob_defectuoso"] for _ in range(config["cantidad_pedido"]))
            inventario += cantidad_recibida
            estado["pedido_en_camino"] = False
            estado["tiempo_entrega"] = 0
            estado["llegada_prevista"] = None

    # 2. Demanda
    rnd_demanda = random.random()
    demanda = generar_variable_discreta(rnd_demanda, config["valores_demanda"], config["prob_demanda"])

    if inventario >= demanda:
        inventario -= demanda
        stockout = 0
    else:
        stockout = demanda - inventario
        inventario = 0

    costo_stockout = stockout * config["costo_stockout"]
    costo_inventario = inventario * config["costo_inventario"]

    # 3. Pedido nuevo
    if not estado["pedido_en_camino"] and inventario <= config["punto_reposicion"]:
        rnd_tiempo = random.random()
        tiempo_estimado = generar_variable_discreta(rnd_tiempo, config["valores_tiempo_entrega"], config["prob_tiempo_entrega"])
        estado["pedido_en_camino"] = True
        estado["tiempo_entrega"] = tiempo_estimado
        estado["llegada_prevista"] = semana + tiempo_estimado
        costo_pedido = config["costo_pedido"]

    estado["inventario"] = inventario

    return {
        "semana": semana,
        "inventario": inventario,
        "rnd_demanda": round(rnd_demanda, 2),
        "demanda": demanda,
        "stockout": stockout,
        "costo_stockout": costo_stockout,
        "rnd_defec": round(rnd_defec, 2) if rnd_defec is not None else None,
        "en condiciones": cantidad_recibida,
        "defectuosos": config["cantidad_pedido"] - cantidad_recibida if llegada_pedido else None,
        "costo_pedido": costo_pedido,
        "rnd_tiempo": round(rnd_tiempo, 2) if rnd_tiempo is not None else None,
        "tiempo_entrega_estimado": tiempo_estimado,
        "llegada_pedido_en": estado.get("llegada_prevista", None),
        "costo_inventario": costo_inventario,
        "costo_total": costo_stockout + costo_inventario + costo_pedido
    }
