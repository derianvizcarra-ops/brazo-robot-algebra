import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("El Reto del Gimbal Lock 🎯")
st.write("Encuentra el ángulo crítico en el Eje Y que hace colapsar el sistema tridimensional.")

# --- CONTROLES DEL RETO ---
st.write("### Paso 1: Fija el Eje Y")
opciones_y = [0, 15, 30, 45, 60, 75, 90, 120, 150, 180]
ry = st.select_slider("Elige un ángulo para el Eje Y:", options=opciones_y, value=0)

st.write("### Paso 2: Prueba los otros ejes")
st.write("Mueve el Eje X y luego el Eje Z. Observa atentamente: ¿En qué ángulo del Eje Y notas que mover X y Z produce exactamente el mismo giro?")
col1, col2 = st.columns(2)
with col1:
    # Añadimos step=20 para saltos más controlados
    rx = st.slider("Mueve el Eje X", -180, 180, 0, step=20)
with col2:
    # Añadimos step=20 para saltos más controlados
    rz = st.slider("Mueve el Eje Z", -180, 180, 0, step=20)

# Convertir a radianes
theta_x = np.radians(rx)
theta_y = np.radians(ry)
theta_z = np.radians(rz)

# --- COLORES ESTÁTICOS DEL AVIÓN ---
color_avion = '#00f2e2' # Cian futurista
color_bordes = '#004d48'

# --- MATRICES DEL GRUPO SO(3) ---
Mx = np.array([[1, 0, 0], [0, np.cos(theta_x), -np.sin(theta_x)], [0, np.sin(theta_x), np.cos(theta_x)]])
My = np.array([[np.cos(theta_y), 0, np.sin(theta_y)], [0, 1, 0], [-np.sin(theta_y), 0, np.cos(theta_y)]])
Mz = np.array([[np.cos(theta_z), -np.sin(theta_z), 0], [np.sin(theta_z), np.cos(theta_z), 0], [0, 0, 1]])

# Multiplicación consecutiva
M_final = np.dot(Mz, np.dot(My, Mx))

# --- DEFINIR EL OBJETO 3D (AVIÓN) ---
# Vértices
vertices = np.array([[0, 3, 0], [0, -2, 0], [-2, -1, 0], [2, -1, 0], [0, -2, 1.5]])
vertices_rotados = np.dot(vertices, M_final.T)

x = vertices_rotados[:, 0]
y = vertices_rotados[:, 1]
z = vertices_rotados[:, 2]

# --- CREAR EL GRÁFICO 3D MEJORADO ---
fig = go.Figure()

i_faces = [0, 0, 0] 
j_faces = [1, 1, 1] 
k_faces = [2, 3, 4] 

fig.add_trace(go.Mesh3d(
    x=x, y=y, z=z,
    i=i_faces, j=j_faces, k=k_faces,
    color=color_avion,
    opacity=0.9,
    flatshading=True,
    lighting=dict(ambient=0.4, diffuse=0.8, roughness=0.5, specular=0.6, fresnel=0.2),
    showscale=False
))

lineas = [(0, 1), (0, 2), (0, 3), (2, 1), (3, 1), (1, 4), (0, 4)]
for inicio, fin in lineas:
    fig.add_trace(go.Scatter3d(
        x=[x[inicio], x[fin]], y=[y[inicio], y[fin]], z=[z[inicio], z[fin]],
        mode='lines', line=dict(color=color_bordes, width=4), showlegend=False, hoverinfo='skip'
    ))

fig.update_layout(
    scene=dict(
        xaxis=dict(range=[-4, 4], title='Eje X', showbackground=False, gridcolor='gray'),
        yaxis=dict(range=[-4, 4], title='Eje Y', showbackground=False, gridcolor='gray'),
        zaxis=dict(range=[-4, 4], title='Eje Z', showbackground=False, gridcolor='gray'),
        aspectmode='cube',
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)) 
    ),
    margin=dict(l=0, r=0, b=0, t=0), height=550,
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig, use_container_width=True)

# --- LA REVELACIÓN MATEMÁTICA ---
st.write("---")
# Usamos un expansor para ocultar las matrices hasta el momento adecuado
with st.expander("Haz clic aquí para ver la demostración matemática (El código Matrix)"):
    st.write("Cada movimiento de los deslizadores es en realidad una matriz del grupo $SO(3)$.")
    
    # Función para limpiar y formatear la matriz
    def matriz_a_latex(matriz):
        lineas = []
        for fila in matriz:
            fila_formateada = []
            for valor in fila:
                # Evita el "-0.00" por errores de precisión de punto flotante
                valor_limpio = 0.0 if abs(valor) < 1e-10 else valor
                fila_formateada.append(f"{valor_limpio:.2f}")
            lineas.append(" & ".join(fila_formateada))
        return r"\begin{bmatrix} " + r" \\ ".join(lineas) + r" \end{bmatrix}"

    st.latex(r"M_{EjeX} = " + matriz_a_latex(Mx))
    st.latex(r"M_{EjeY} = " + matriz_a_latex(My))
    st.latex(r"M_{EjeZ} = " + matriz_a_latex(Mz))

    st.write("Al aplicar la propiedad de clausura (multiplicar), la computadora obtiene la **Matriz Final**:")
    st.latex(r"M_{final} = M_z \cdot M_y \cdot M_x = " + matriz_a_latex(M_final))
    
    st.info("💡 **Observación:** Cuando el Eje Y está en (el angulo hallado), mueve X y luego Z. Verás que los números dentro de la $M_{final}$ cambian de forma idéntica o complementaria. ¡Las matrices han perdido independencia lineal!")
    st.info("Elaborado por: Derian Vizcarra - 2026")