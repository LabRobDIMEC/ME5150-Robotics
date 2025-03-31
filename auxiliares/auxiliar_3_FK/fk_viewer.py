import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def forward_kinematics(theta1, theta2, theta3, L1=1, L2=1, L3=1):
    """Calcula las coordenadas del extremo del robot de 2 links."""
    x0, y0 = 0, 0  # Base del robot
    x1 = L1 * np.cos(np.radians(theta1))
    y1 = L1 * np.sin(np.radians(theta1))
    x2 = x1 + L2 * np.cos(np.radians(theta1 + theta2))
    y2 = y1 + L2 * np.sin(np.radians(theta1 + theta2))
    x3 = x2 + L3 * np.cos(np.radians(theta1 + theta2 + theta3))
    y3 = y2 + L3 * np.sin(np.radians(theta1 + theta2 + theta3))

    print(x3, y3)
    
    return [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]

# Inicialización de la figura y los ejes
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.2, bottom=0.25)
ax.set_xlim(0, 3)
ax.set_ylim(0, 3)
ax.set_aspect('equal')
ax.grid()
plt.title("ho")

# Valores iniciales
theta1_0, theta2_0, theta3_0 = 45, 30, 15
puntos = forward_kinematics(theta1_0, theta2_0, theta3_0)

# Graficar el robot
line, = ax.plot([p[0] for p in puntos], [p[1] for p in puntos], 'o-', markersize=8, lw=3)

# Agregar sliders para los ángulos
theta1_ax = plt.axes([0.2, 0.15, 0.65, 0.03])
theta2_ax = plt.axes([0.2, 0.10, 0.65, 0.03])
theta3_ax = plt.axes([0.2, 0.05, 0.65, 0.03])
slider_theta1 = Slider(theta1_ax, 'Theta1', -180, 180, valinit=theta1_0)
slider_theta2 = Slider(theta2_ax, 'Theta2', -180, 180, valinit=theta2_0)
slider_theta3 = Slider(theta3_ax, 'Theta3', -180, 180, valinit=theta3_0)


def update(val):
    """Actualiza la posición del robot cuando se mueven los sliders."""
    theta1 = slider_theta1.val
    theta2 = slider_theta2.val
    theta3 = slider_theta3.val
    puntos = forward_kinematics(theta1, theta2, theta3)
    line.set_xdata([p[0] for p in puntos])
    line.set_ydata([p[1] for p in puntos])
    fig.canvas.draw_idle()
    plt.title(str(puntos))

# Conectar sliders con la función de actualización
slider_theta1.on_changed(update)
slider_theta2.on_changed(update)
slider_theta3.on_changed(update)

plt.show()