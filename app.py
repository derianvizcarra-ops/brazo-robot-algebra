import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Cinemática del Brazo Robótico 🦾")
st.write("Aplicación del Grupo de Transformaciones Especiales")

# Deslizadores para que el usuario interactúe
theta1 = st.slider("Ángulo del Hombro", 0, 180, 45)
theta2 = st.slider("Ángulo del Codo", -180, 180, 45)

# Convertir a radianes
t1 = np.radians(theta1)
t2 = np.radians(theta2)

# Longitud de los segmentos del brazo
L1 = 5
L2 = 4

# Matrices de transformación (Operaciones del Grupo)
# Matriz del hombro
M1 = np.array([
    [np.cos(t1), -np.sin(t1), L1 * np.cos(t1)],
    [np.sin(t1),  np.cos(t1), L1 * np.sin(t1)],
    [0,           0,          1]
])

# Matriz del codo
M2 = np.array([
    [np.cos(t2), -np.sin(t2), L2 * np.cos(t2)],
    [np.sin(t2),  np.cos(t2), L2 * np.sin(t2)],
    [0,           0,          1]
])

# Propiedad de Clausura: Multiplicamos las matrices
M_final = np.dot(M1, M2)

# Coordenadas para dibujar
origen = [0, 0]
codo = [M1[0, 2], M1[1, 2]]
mano = [M_final[0, 2], M_final[1, 2]]

x_coords = [origen[0], codo[0], mano[0]]
y_coords = [origen[1], codo[1], mano[1]]

# Crear el gráfico
fig, ax = plt.subplots()
ax.plot(x_coords, y_coords, marker='o', linewidth=4, markersize=10, color='#ff4b4b')
ax.set_xlim(-10, 10)
ax.set_ylim(-2, 10)
ax.grid(True)

# Mostrar un único gráfico en Streamlit
st.pyplot(fig)

# --- CÓDIGO PARA MOSTRAR LAS MATRICES ---
st.write("### Multiplicación de Matrices en Tiempo Real:")

# Función para convertir las matrices a formato matemático elegante
def matriz_a_latex(matriz):
    lineas = []
    for fila in matriz:
        # Redondeamos a 2 decimales para que se vea limpio
        fila_formateada = " & ".join([f"{valor:.2f}" for valor in fila])
        lineas.append(fila_formateada)
    return r"\begin{bmatrix} " + r" \\ ".join(lineas) + r" \end{bmatrix}"

# Mostramos las matrices en la pantalla
st.latex(r"M_{hombro} = " + matriz_a_latex(M1))
st.latex(r"M_{codo} = " + matriz_a_latex(M2))

st.write("Aplicando la clausura del grupo (multiplicamos):")
st.latex(r"M_{final} = M_{hombro} \cdot M_{codo} = " + matriz_a_latex(M_final))