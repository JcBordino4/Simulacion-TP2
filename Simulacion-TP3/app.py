import streamlit as st
import pandas as pd
from simulacion_inventario_montecarlo import simular_semana

# ----------------------------- INTERFAZ ------------------------------ #
st.title("Simulación Montecarlo - Librería Campus XXI")

st.sidebar.header("Parámetros del sistema")

# Entradas del usuario
st.sidebar.subheader("Probabilidades demanda")
prob_0 = st.sidebar.number_input("P(0 libros)", min_value=0.0, max_value=1.0, value=0.50, step=0.05)
prob_1 = st.sidebar.number_input("P(1 libro)", min_value=0.0, max_value=1.0, value=0.15, step=0.05)
prob_2 = st.sidebar.number_input("P(2 libros)", min_value=0.0, max_value=1.0, value=0.25, step=0.05)
prob_3 = st.sidebar.number_input("P(3 libros)", min_value=0.0, max_value=1.0, value=0.10, step=0.05)

valores_demanda = [0, 1, 2, 3]
prob_demanda = [prob_0, prob_1, prob_2, prob_3]
if sum(prob_demanda) != 1.0:
    st.error("Las probabilidades de demanda no suman 100%")

st.sidebar.subheader("Probabilidades tiempo entrega")
prob_t1 = st.sidebar.number_input("P(1 semana)", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
prob_t2 = st.sidebar.number_input("P(2 semanas)", min_value=0.0, max_value=1.0, value=0.4, step=0.05)
prob_t3 = st.sidebar.number_input("P(3 semanas)", min_value=0.0, max_value=1.0, value=0.3, step=0.05)

valores_tiempo = [1, 2 ,3]
prob_tiempo = [prob_t1, prob_t2, prob_t3]
if sum(prob_tiempo) != 1.0:
    st.error("Las probabilidades de tiempo no suman 100%")

prob_defectuoso = 1 - (st.sidebar.slider("Porcentaje en condiciones", 0, 100, 80) / 100)

st.sidebar.subheader("Costos")
costo_inventario = st.sidebar.number_input("Costo de inventario", value=30)
costo_pedido = st.sidebar.number_input("Costo de pedido", value=200)
costo_stockout = st.sidebar.number_input("Costo de stockout", value=50)

st.sidebar.subheader("Condiciones")
inventario_inicial = st.sidebar.number_input("Inventario inicial", value=7)
punto_reposicion = st.sidebar.number_input("Punto de reposición", value=2)
cantidad_pedido = st.sidebar.number_input("Cantidad a pedir", value=5)

st.sidebar.subheader("Configuraciones de la simulación")
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

    st.subheader("Costo promedio por semana")
    st.metric("Promedio", f"${(df['costo_acumulado']/n_semanas).iloc[-1]:,.2f}")

