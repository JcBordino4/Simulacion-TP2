import streamlit as st

st.title("Simulación de Inventario - Librería Campus XXI")

st.header("Parámetros de Simulación")

# Parámetros ingresables
prob_demandas = st.text_input("Probabilidades de demanda (ej: 50,15,25,10)", "50,15,25,10")
prob_entregas = st.text_input("Probabilidades de tiempo de entrega (ej: 0.3,0.4,0.3)", "0.3,0.4,0.3")
prob_defectuosos = st.slider("Probabilidad de libro defectuoso (%)", 0, 100, 20)

costo_tenencia = st.number_input("Costo de tenencia ($/libro/semana)", value=30)
costo_pedido = st.number_input("Costo de pedido ($)", value=200)
costo_agotamiento = st.number_input("Costo de agotamiento ($/libro)", value=50)

inventario_inicial = st.number_input("Inventario inicial (libros)", value=7)
punto_reposicion = st.number_input("Punto de reposición (libros)", value=2)
cantidad_reposicion = st.number_input("Cantidad a reponer", value=5)

# Parámetros de simulación
semanas_a_simular = st.number_input("Cantidad de semanas a simular (N)", value=100000)
mostrar_desde = st.number_input("Mostrar vector desde la semana (j)", value=0)
mostrar_cantidad = st.number_input("Cantidad de filas a mostrar (i)", value=10)

if st.button("Ejecutar Simulación"):
    st.write("Acá iría la lógica de la simulación")
    # df_resultado = simular(...)
    # st.dataframe(df_resultado.iloc[mostrar_desde:mostrar_desde+mostrar_cantidad])
