import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="centered")

st.title("Reto: El Laberinto Matemático 🧭")
st.write("Demuestra que en la computación gráfica, **el orden de los factores SÍ altera el producto**. Programa la trayectoria correcta para que el robot llegue a la meta.")

# --- OPCIONES DEL RETO ---
acciones_nombres = [
    "--- Selecciona una acción ---",
    "Avanzar 4 metros (T4)",
    "Girar 90° a la Izquierda (R90)",
    "Avanzar 3 metros (T3)"
]

col1, col2, col3 = st.columns(3)
with col1:
    paso1 = st.selectbox("Acción 1:", acciones_nombres, index=0)
with col2:
    paso2 = st.selectbox("Acción 2:", acciones_nombres, index=0)
with col3:
    paso3 = st.selectbox("Acción 3:", acciones_nombres, index=0)

# --- MATRICES DE TRANSFORMACIÓN LOCAL SE(2) ---
# T(x): Matriz de traslación
def matriz_T(distancia):
    return np.array([[1, 0, distancia], [0, 1, 0], [0, 0, 1]])

# R(theta): Matriz de rotación
def matriz_R(grados):
    rad = np.radians(grados)
    return np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0, 0, 1]])

# Diccionario de acciones a matrices
matrices_dict = {
    "Avanzar 4 metros (T4)": matriz_T(4),
    "Girar 90° a la Izquierda (R90)": matriz_R(90),
    "Avanzar 3 metros (T3)": matriz_T(3)
}

# --- CÁLCULO DE LA TRAYECTORIA ---
# Estado inicial (Origen)
M_actual = np.eye(3)
puntos_x, puntos_y = [0], [0]

secuencia = [paso1, paso2, paso3]
for accion in secuencia:
    if accion != "--- Selecciona una acción ---":
        # Multiplicación matricial (Propiedad de clausura del grupo)
        M_actual = M_actual @ matrices_dict[accion]
        puntos_x.append(M_actual[0, 2])
        puntos_y.append(M_actual[1, 2])

# --- VERIFICACIÓN DE VICTORIA ---
target_x, target_y = 4, 3
if len(puntos_x) == 4 and abs(puntos_x[-1] - target_x) < 0.1 and abs(puntos_y[-1] - target_y) < 0.1:
    st.success("¡RETO COMPLETADO! Has descubierto el orden matemático correcto.")
    color_linea = "#00ff88"
else:
    color_linea = "#00c3ff"

# --- GRÁFICO DE TRAYECTORIA EN PLOTLY ---
fig = go.Figure()

# Dibujar la ruta
fig.add_trace(go.Scatter(
    x=puntos_x, y=puntos_y,
    mode='lines+markers',
    line=dict(color=color_linea, width=6, dash='dot'),
    marker=dict(size=12, color='white'),
    name='Trayectoria del Robot'
))

# Dibujar Punto de Inicio
fig.add_trace(go.Scatter(
    x=[0], y=[0], mode='markers',
    marker=dict(symbol='square', size=20, color='blue'), name='Inicio'
))

# Dibujar Meta
fig.add_trace(go.Scatter(
    x=[target_x], y=[target_y], mode='markers+text',
    marker=dict(symbol='star', size=35, color='#ffd700', line=dict(color='#ff8c00', width=2)),
    text=["Meta"], textposition="top center", name='Meta'
))

fig.update_layout(
    xaxis=dict(range=[-1, 8], title="Coordenada X", showgrid=True),
    yaxis=dict(range=[-1, 8], title="Coordenada Y", showgrid=True),
    height=500, margin=dict(l=0, r=0, t=30, b=0),
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# --- REVELACIÓN MATEMÁTICA ---
with st.expander("🔍 Ver Demostración del Grupo No Abeliano"):
    st.write("Si el grupo de traslaciones y rotaciones fuera abeliano, daría igual el orden de los comandos. Pero en $SE(2)$, las matrices nos demuestran que **el orden altera el producto**:")
    
    def format_matrix(m):
        lines = [" & ".join([f"{0.0 if abs(v) < 1e-10 else v:.2f}" for v in row]) for row in m]
        return r"\begin{bmatrix} " + r" \\ ".join(lines) + r" \end{bmatrix}"
    
    st.latex(r"T_4 = " + format_matrix(matriz_T(4)) + r"\quad R_{90} = " + format_matrix(matriz_R(90)))
    
    st.write("Comparación de multiplicaciones:")
    M_T4_R90 = matriz_T(4) @ matriz_R(90)
    M_R90_T4 = matriz_R(90) @ matriz_T(4)
    
    st.latex(r"T_4 \cdot R_{90} = " + format_matrix(M_T4_R90))
    st.latex(r"R_{90} \cdot T_4 = " + format_matrix(M_R90_T4))
    
    st.error("Como puedes ver, los resultados en la última columna (que representan las coordenadas finales) son completamente distintos. Por eso las computadoras son tan estrictas con el orden al renderizar gráficos.")

st.markdown("<div style='text-align: right; color: gray; margin-top: 20px;'><em>Elaborado por Derian Vizcarra</em></div>", unsafe_allow_html=True)