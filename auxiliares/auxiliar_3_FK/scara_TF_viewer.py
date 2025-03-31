import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

class PoseViewer:

    def __init__(self):
        self.q = [0, 0, 0, 0]  # q1, q2, q3 (altura)
        self.poses = np.array([])
        self.ax3 = None

    def get_pose_to_origin_pose(self):
        q1, q2, q3 = np.radians(self.q[0]), np.radians(self.q[1]), self.q[2]  # Convertir ángulos a radianes
        l0, l1, l2 = [200, 200, 200]

        # Matriz identidad para el origen
        origin = np.identity(4)

        # Transformaciones homogéneas
        T01 = self.traslation(z=l0) @ self.rot_z(q1)  # Base girando en q1
        T12 = self.traslation(x=l1) @ self.rot_z(q2)  # Brazo girando en q2
        T23 = self.traslation(x=l2)  # Segundo brazo (sin más rotación)
        T34 = self.traslation(z=-q3)  # Movimiento lineal del efector final

        # Cálculo de las posiciones acumuladas
        H1 = T01  # Base
        H2 = H1 @ T12  # Codo
        H3 = H2 @ T23  # Muñeca
        H4 = H3 @ T34  # Efector final

        self.poses = np.array([origin, H1, H2, H3, H4])

    def traslation(self, x=0, y=0, z=0):
        return np.array([[1, 0, 0, x],
                         [0, 1, 0, y],
                         [0, 0, 1, z],
                         [0, 0, 0, 1]])  

    def rot_z(self, qz):
        return np.array([[np.cos(qz), -np.sin(qz), 0, 0],
                         [np.sin(qz), np.cos(qz), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

    def draw_axes_tf(self, poses):
        self.ax3.clear()
        self.ax3.set_xlim(-400, 400)
        self.ax3.set_ylim(-400, 400)
        self.ax3.set_zlim(0, 400)
        self.ax3.set_title("Robot SCARA")
        self.ax3.set_xlabel('X-axis')
        self.ax3.set_ylabel('Y-axis')
        self.ax3.set_zlabel('Z-axis')

        for pose in poses:
            origin_pose = pose[:3, 3]
            x_rot = pose[:3, 0]  # Eje X
            y_rot = pose[:3, 1]  # Eje Y
            z_rot = pose[:3, 2]  # Eje Z

            self.ax3.quiver(origin_pose[0], origin_pose[1], origin_pose[2],
                            x_rot[0], x_rot[1], x_rot[2], length=50, color='r')
            self.ax3.quiver(origin_pose[0], origin_pose[1], origin_pose[2],
                            y_rot[0], y_rot[1], y_rot[2], length=50, color='g')
            self.ax3.quiver(origin_pose[0], origin_pose[1], origin_pose[2],
                            z_rot[0], z_rot[1], z_rot[2], length=50, color='b')

            self.ax3.scatter(origin_pose[0], origin_pose[1], origin_pose[2], color='k', s=10)

    def slider(self):
        fig = plt.figure(figsize=(6, 8))
        self.ax3 = fig.add_subplot(111, projection='3d')
        self.get_pose_to_origin_pose()
        self.draw_axes_tf(self.poses)

        # Creación de sliders
        self.slider1_ax = plt.axes([0.2, 0.1, 0.65, 0.03])
        self.slider2_ax = plt.axes([0.2, 0.15, 0.65, 0.03])
        self.slider3_ax = plt.axes([0.2, 0.2, 0.65, 0.03])
        resetax = plt.axes([0.8, 0.025, 0.1, 0.04])

        self.slider1 = Slider(self.slider1_ax, 'q1', -90, 90, valinit=0)
        self.slider2 = Slider(self.slider2_ax, 'q2', -90, 90, valinit=0)
        self.slider3 = Slider(self.slider3_ax, 'q3', 0, 100, valinit=0)

        button = plt.Button(resetax, 'Reset', color='white', hovercolor='0.975')
        button.on_clicked(self.reset)
        self.slider1.on_changed(self.update)
        self.slider2.on_changed(self.update)
        self.slider3.on_changed(self.update)
        plt.show()

    def update(self, val):
        self.q = [self.slider1.val, self.slider2.val, self.slider3.val]
        self.get_pose_to_origin_pose()
        self.draw_axes_tf(self.poses)

    def reset(self, event):
        self.slider1.reset()
        self.slider2.reset()
        self.slider3.reset()

if __name__ == "__main__":
    robot = PoseViewer()
    robot.slider()
