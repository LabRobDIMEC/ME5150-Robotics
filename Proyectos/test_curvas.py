import numpy as np
import matplotlib.pyplot as plt














# p es el número de divisiones entre los puntos
def generar_recta_p(x1, y1, x2, y2, p):
    x_recta = []
    y_recta = []


    for i in range(p + 1):
        t = i / p
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        x_recta.append(x)
        y_recta.append(y)

    return x_recta, y_recta
















### -----  ARCO GENERADO ENTRE DOS PUNTOS


def generar_arco_p(x1, y1, x2, y2, p):

    # Punto medio entre los extremos → centro del círculo
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2

    # Radio: mitad de la distancia entre los puntos
    dx = x2 - x1
    dy = y2 - y1
    r = np.sqrt(dx**2 + dy**2) / 2

    # Ángulo de la recta (dirección del diámetro)
    ang0 = np.arctan2(dy, dx)

    # El arco va desde ang0 + π a ang0 (semicírculo)
    xs = []
    ys = []

    for i in range(p + 1):
        t = i / p
        ang = ang0 + np.pi * (1 - t)  # Interpola desde ang0 + π a ang0
        x = cx + r * np.cos(ang)
        y = cy + r * np.sin(ang)
        xs.append(x)
        ys.append(y)

    return xs, ys

#BEZIER SEGUNDO ORDEN
def generar_bezier_p(x1, y1, x2, y2, xc, yc, p):

    xs = []
    ys = []

    for i in range(p + 1):
        t = i / p
        x = (1 - t)**2 * x1 + 2 * (1 - t) * t * xc + t**2 * x2
        y = (1 - t)**2 * y1 + 2 * (1 - t) * t * yc + t**2 * y2
        xs.append(x)
        ys.append(y)

    return xs, ys


#BEZIER TERCER ORDEN
def generar_bezier_cubica_p(x1, y1, x2, y2, xc1, yc1, xc2, yc2, p):
    xs = []
    ys = []

    for i in range(p + 1):
        t = i / p
        u = 1 - t

        x = (u**3) * x1 + 3 * (u**2) * t * xc1 + 3 * u * (t**2) * xc2 + (t**3) * x2
        y = (u**3) * y1 + 3 * (u**2) * t * yc1 + 3 * u * (t**2) * yc2 + (t**3) * y2

        xs.append(x)
        ys.append(y)

    return xs, ys





### ---- para graficar

def graficar_puntos(xs, ys, titulo=' '):

    plt.figure(figsize=(6, 4))
    plt.plot(xs, ys, marker='o', linestyle='-', color='blue', label='Interpolación lineal')
    plt.scatter([xs[0], xs[-1]], [ys[0], ys[-1]], color='red', zorder=5, label='Puntos extremos')
    
    plt.title(titulo)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.show()






#Caso:


xs, ys = generar_bezier_cubica_p(0, 0, 10, 0, 2, 5, 8, -5, p=10)
graficar_puntos(xs, ys, titulo='Curva de Bézier cúbica')


