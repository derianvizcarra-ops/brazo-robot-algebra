import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="centered")

st.title("Reto: Cinemática Inversa 🤖")
st.write("En la industria, no programamos ángulos; programamos la **coordenada exacta** donde el robot debe trabajar. Tu misión es encontrar los ángulos para alcanzar la estrella.")

# --- OBJETIVO FIJO ---
target_x, target_y = -3, 4
L1, L2 = 4, 3 # Longitud de los eslabones

col1, col2 = st.columns(2)
with col1:
    ang_hombro = st.slider("Motor Hombro (Grados)", -180, 180, 0, step=5)
with col2:
    ang_codo = st.slider("Motor Codo (Grados)", -180, 180, 0, step=5)

t1 = np.radians(ang_hombro)
t2 = np.radians(ang_codo)

# --- MATRICES HOMOGÉNEAS SE(2) ---
# Matriz de Rotación del Hombro
R_hombro = np.array([[np.cos(t1), -np.sin(t1), 0], [np.sin(t1), np.cos(t1), 0], [0, 0, 1]])
# Traslación por el primer eslabón
T_eslabon1 = np.array([[1, 0, L1], [0, 1, 0], [0, 0, 1]])
# Matriz de Rotación del Codo
R_codo = np.array([[np.cos(t2), -np.sin(t2), 0], [np.sin(t2), np.cos(t2), 0], [0, 0, 1]])
# Traslación por el segundo eslabón
T_eslabon2 = np.array([[1, 0, L2], [0, 1, 0], [0, 0, 1]])

# Multiplicación en cadena (Cinemática Directa)
M_codo_base = R_hombro @ T_eslabon1
M_final = M_codo_base @ R_codo @ T_eslabon2

# Extraer coordenadas
x0, y0 = 0, 0
x1, y1 = M_codo_base[0, 2], M_codo_base[1, 2]
x2, y2 = M_final[0, 2], M_final[1, 2]

# --- VERIFICACIÓN DE VICTORIA ---
distancia = np.sqrt((x2 - target_x)**2 + (y2 - target_y)**2)
if distancia < 0.5:
    st.success("¡RETO COMPLETADO! Has alcanzado la coordenada objetivo.")
    color_brazo = "#00ff88"
else:
    color_brazo = "#ff4b4b"

# --- GRÁFICO PROFESIONAL EN PLOTLY ---
fig = go.Figure()

# Dibujar Brazo Sólido (Líneas muy gruesas)
fig.add_trace(go.Scatter(
    x=[x0, x1, x2], y=[y0, y1, y2],
    mode='lines+markers',
    line=dict(color=color_brazo, width=15),
    marker=dict(color='white', size=20, line=dict(color='#333', width=4)),
    name='Brazo Robótico'
))

# Dibujar Objetivo (Estrella Visual)
fig.add_trace(go.Scatter(
    x=[target_x], y=[target_y],
    mode='markers+text',
    marker=dict(symbol='star', size=35, color='#ffd700', line=dict(color='#ff8c00', width=2)),
    text=["Meta (-3, 4)"], textposition="top center",
    name='Objetivo'
))

fig.update_layout(
    xaxis=dict(range=[-8, 8], title="Eje X", showgrid=True),
    yaxis=dict(range=[-2, 8], title="Eje Y", showgrid=True),
    height=500, margin=dict(l=0, r=0, t=30, b=0),
    plot_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# --- REVELACIÓN MATEMÁTICA ---
with st.expander("🔍 Ver Operaciones de Matrices (Cinemática y Matriz Inversa)"):
    st.write("Para calcular esto automáticamente, las computadoras usan coordenadas homogéneas de $3 \\times 3$ del grupo $SE(2)$:")
    
    def format_matrix(m):
        lines = [" & ".join([f"{0.0 if abs(v) < 1e-10 else v:.2f}" for v in row]) for row in m]
        return r"\begin{bmatrix} " + r" \\ ".join(lines) + r" \end{bmatrix}"
    
    st.latex(r"M_{final} = R_{hombro} \cdot T_1 \cdot R_{codo} \cdot T_2 = " + format_matrix(M_final))
    
    st.write("La coordenada de la punta del brazo se encuentra en la última columna de la matriz final.")
    st.write("Para hacer que el brazo regrese a su origen exacto, la computadora aplica la **Matriz Inversa** $M_{final}^{-1}$:")
    
    M_inv = np.linalg.inv(M_final)
    st.latex(r"M_{final}^{-1} = " + format_matrix(M_inv))

st.markdown("<div style='text-align: right; color: gray; margin-top: 20px;'><em>Elaborado por Derian Vizcarra</em></div>", unsafe_allow_html=True)