import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------------- CONFIGURACIÓN ----------------
a2 = 1.0  # Longitud primer eslabón
a3 = 1.0  # Longitud segundo eslabón
d1 = 1.0  # Altura base

# ------------- CINEMÁTICA DIRECTA -------------
def F(q):
    """
    Cinemática directa del manipulador SCARA con 3 ángulos.
    q: [theta1, theta2, theta3] en radianes
    return: [x, y, z]
    """
    theta1, theta2, theta3 = q
    x = (a2 * np.cos(theta2) + a3 * np.cos(theta2 + theta3)) * np.cos(theta1)
    y = (a2 * np.cos(theta2) + a3 * np.cos(theta2 + theta3)) * np.sin(theta1)
    z = d1 + a2 * np.sin(theta2) + a3 * np.sin(theta2 + theta3)
    return np.array([x, y, z])

# ------------- JACOBIANO NUMÉRICO -------------
def jacobian(f, x, epsilon=1e-5):
    n = len(x)
    J = np.zeros((len(f(x)), n))
    f_x = f(x)
    for i in range(n):
        dx = np.zeros(n)
        dx[i] = epsilon
        J[:, i] = (f(x + dx) - f_x) / epsilon
    return J

# ------------- MÉTODO DE NEWTON-RAPHSON -------------
def NewtonRaphson(f, q0, target_pos, tol=1e-4, max_iter=100):
    q = q0
    for _ in range(max_iter):
        J = jacobian(f, q)
        try:
            J_inv = np.linalg.inv(J)
        except np.linalg.LinAlgError:
            J_inv = np.linalg.pinv(J)
        q_new = q - J_inv @ (f(q) - target_pos)
        if np.linalg.norm(q_new - q) < tol:
            return q_new
        q = q_new
    raise ValueError("No se encontró solución después de %d iteraciones" % max_iter)

# ------------- NORMALIZAR ÁNGULOS -------------
def limitar_angulos(q):
    return [
        (q[0] + np.pi) % (2 * np.pi) - np.pi,
        (q[1] + np.pi) % (2 * np.pi) - np.pi,
        (q[2] + np.pi) % (2 * np.pi) - np.pi
    ]

# ------------- VISUALIZACIÓN 3D -------------
def FK_points(q):
    """ Devuelve los puntos (x, y, z) de cada articulación incluyendo el eslabón base vertical """
    theta1, theta2, theta3 = q

    # Primer punto (base en el suelo)
    x0, y0, z0 = 0, 0, 0

    # Segundo punto (fin del eslabón vertical)
    x1, y1, z1 = 0, 0, d1

    # Tercer punto
    x2 = x1 + a2 * np.cos(theta2) * np.cos(theta1)
    y2 = y1 + a2 * np.cos(theta2) * np.sin(theta1)
    z2 = z1 + a2 * np.sin(theta2)

    # Cuarto punto
    x3 = x2 + a3 * np.cos(theta2 + theta3) * np.cos(theta1)
    y3 = y2 + a3 * np.cos(theta2 + theta3) * np.sin(theta1)
    z3 = z2 + a3 * np.sin(theta2 + theta3)

    return np.array([
        [x0, y0, z0],
        [x1, y1, z1],
        [x2, y2, z2],
        [x3, y3, z3]
    ])


def plot_robot_3D(joint_points, target_point=None, q_sol_deg=None):
    """ Dibuja el robot en 3D usando matplotlib """
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    xs, ys, zs = joint_points[:, 0], joint_points[:, 1], joint_points[:, 2]
    ax.plot(xs, ys, zs, '-o', linewidth=4, markersize=8, label='SCARA')

    # Punto objetivo
    if target_point is not None:
        ax.scatter(*target_point, color='red', s=80, label='Objetivo')

        # Dibuja una flecha desde la base (o último joint) hacia el target
        base = joint_points[-1]
        direction = target_point - base
        ax.quiver(base[0], base[1], base[2],
                  direction[0], direction[1], direction[2],
                  color='green', arrow_length_ratio=0.1, linewidth=2, label='Vector al objetivo')

    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([0, 3])
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Visualización SCARA en 3D')
    ax.legend()
    ax.view_init(elev=30, azim=45)

    if q_sol_deg is not None:
        text = f"θ1 = {q_sol_deg[0]:.1f}°\nθ2 = {q_sol_deg[1]:.1f}°\nθ3 = {q_sol_deg[2]:.1f}°"
        ax.text2D(0.02, 0.95, text, transform=ax.transAxes, fontsize=10, verticalalignment='top')

    plt.tight_layout()
    plt.show()



# ------------- MAIN -------------
def main():
    target = np.array([0.5, 0, 2.0])  # Cambia el objetivo si lo deseas
    q0 = np.array([0.1, 0.1, 0.1])       # Semilla inicial

    try:
        q_sol = NewtonRaphson(F, q0, target)
        q_sol = limitar_angulos(q_sol)
        q_sol_deg = np.degrees(q_sol)

        print("Solución IK (rad):", q_sol)
        print("Solución IK (°):", q_sol_deg)

        puntos = FK_points(q_sol)
        plot_robot_3D(puntos, target, q_sol_deg)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
