import streamlit as st
import pandas as pd
from simulacion_inventario_montecarlo import simular_semana

# ----------------------------- INTERFAZ ------------------------------ #
st.title("Simulación Montecarlo - Librería Campus XXI")

st.sidebar.header("Parámetros del sistema")

# Entradas del usuario
valores_demanda = [0, 1, 2, 3]
try:
    prob_demanda = [float(x.strip()) / 100 for x in st.sidebar.text_input("Probabilidades demanda (%)", "50,15,25,10").split(",")]
except ValueError:
    st.error("⚠️ Asegurate de ingresar números separados por comas, ej: 50,15,25,10")
    prob_demanda = []

valores_tiempo = [1, 2, 3]
prob_tiempo = [float(x) for x in st.sidebar.text_input("Probabilidades tiempo entrega", "0.3,0.4,0.3").split(",")]

prob_defectuoso = 1 - (st.sidebar.slider("Porcentaje en condiciones", 0, 100, 80) / 100)

costo_inventario = st.sidebar.number_input("Costo de inventario", value=30)
costo_pedido = st.sidebar.number_input("Costo de pedido", value=200)
costo_stockout = st.sidebar.number_input("Costo de stockout", value=50)

inventario_inicial = st.sidebar.number_input("Inventario inicial", value=7)
punto_reposicion = st.sidebar.number_input("Punto de reposición", value=2)
cantidad_pedido = st.sidebar.number_input("Cantidad a pedir", value=5)

n_semanas = st.sidebar.number_input("Cantidad de semanas a simular", value=100)

mostrar_desde = st.sidebar.number_input("Mostrar desde semana", value=0)
mostrar_cant = st.sidebar.number_input("Cantidad de semanas a mostrar", value=20)

# ------------------------- EJECUTAR SIMULACIÓN ------------------------ #
if st.button("▶ Ejecutar simulación"):
    config = {
        "valores_demanda": valores_demanda,
        "prob_demanda": prob_demanda,
        "valores_tiempo_entrega": valores_tiempo,
        "prob_tiempo_entrega": prob_tiempo,
        "prob_defectuoso": prob_defectuoso,
        "costo_inventario": costo_inventario,
        "costo_pedido": costo_pedido,
        "costo_stockout": costo_stockout,
        "punto_reposicion": punto_reposicion,
        "cantidad_pedido": cantidad_pedido
    }

    estado = {
        "inventario": inventario_inicial,
        "pedido_en_camino": False,
        "tiempo_entrega": 0
    }

    resultados = []
    costo_acumulado = 0
    for semana in range(n_semanas):
        fila = simular_semana(semana + 1, estado, config)
        costo_acumulado += fila["costo_total"]
        fila["costo_acumulado"] = costo_acumulado
        resultados.append(fila)

    df = pd.DataFrame(resultados)

    st.subheader("Resultados")
    df_mostrar = df.iloc[int(mostrar_desde):int(mostrar_desde) + int(mostrar_cant)]
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

    st.subheader("Fila final (última semana)")
    st.write(df.iloc[-1:])

    st.subheader("Costo total acumulado")
    st.metric("Total", f"${df['costo_acumulado'].iloc[-1]:,.2f}")

