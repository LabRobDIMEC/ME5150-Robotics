import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

class PoseViewer:

    def __init__(self):
        self.q = [0, 0, 0, 0, 0, 0]  # 6 grados de acción, inicialmente en "cero"
        self.poses = np.array([])
        self.ax3 = None

    def get_pose_to_origin_pose(self):

        # convertimos los "q" a radianes.
        q1, q2, q3, q4, q5, q6 = np.radians(self.q)
        

        # matriz diagonal identidad para indicar el origen.
        origin = np.identity(4)


        #Transformaciones del robot.
        T01 = self.traslation(z=27.5) @ self.rot_z(q1)
        T12 = self.traslation(z=40) @ self.rot_y(q2)
        T23 = self.traslation(z=75) @ self.rot_y(q3)
        T34 = self.traslation(z=75) @ self.rot_y(q4)
        T45 = self.traslation(z=75) @ self.rot_x(q5)
        T56 = self.traslation(x=75)

        #Productos puntos parciales para las poses de cada joint.
        H1 = T01 #pose J1
        H2 = H1 @ T12 #pose J2
        H3 = H2 @ T23 #pose J3
        H4 = H3 @ T34 #pose J4
        H5 = H4 @ T45 #pose J5
        H6 = H5 @ T56 #pose J6 o efector en este caso.
        print(H6) 

        #producto punto para visualización.
        self.poses = np.array([origin, H1, H2, H3, H4, H5, H6])
        

    #--- Matrices de Transformación Homogenea ---#

    # Traslación:
    def traslation(self, x=0, y=0, z=0):
        return np.array([[1, 0, 0, x],
                         [0, 1, 0, y],
                         [0, 0, 1, z],
                         [0, 0, 0, 1]])
    
    # Rotación en X:
    def rot_x(self, qx):
        return np.array([[1, 0, 0, 0],
                         [0, np.cos(qx), -np.sin(qx), 0],
                         [0, np.sin(qx), np.cos(qx), 0],
                         [0, 0, 0, 1]])

    # Rotación en Y:
    def rot_y(self, qy):
        return np.array([[np.cos(qy), 0, np.sin(qy), 0],
                         [0, 1, 0, 0],
                         [-np.sin(qy), 0, np.cos(qy), 0],
                         [0, 0, 0, 1]])

    # Rotación en Z:
    def rot_z(self, qz):
        return np.array([[np.cos(qz), -np.sin(qz), 0, 0],
                         [np.sin(qz), np.cos(qz), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
    
    # --- fin matrices de transformación homogenea --- #


    ## --- Funciones para visualización --- ##
    def draw_axes_tf(self, poses):
        self.ax3.clear()
        self.ax3.set_xlim(-400, 400)
        self.ax3.set_ylim(-400, 400)
        self.ax3.set_zlim(0, 400)
        self.ax3.set_title("Robot")
        self.ax3.set_xlabel('X-axis')
        self.ax3.set_ylabel('Y-axis')
        self.ax3.set_zlabel('Z-axis')

        for pose in poses:
            origin_pose = pose[:3, 3]
            x_rot = pose[:3, 0]
            y_rot = pose[:3, 1]
            z_rot = pose[:3, 2]

            self.ax3.quiver(*origin_pose, *x_rot, length=50, color='r')
            self.ax3.quiver(*origin_pose, *y_rot, length=50, color='g')
            self.ax3.quiver(*origin_pose, *z_rot, length=50, color='b')
            self.ax3.scatter(*origin_pose, color='k', s=10)

    def slider(self):
        fig = plt.figure(figsize=(8, 10))
        self.ax3 = fig.add_subplot(211, projection='3d')  # Parte superior

        self.get_pose_to_origin_pose()
        self.draw_axes_tf(self.poses)

        # Ejes de los sliders en la parte inferior
        slider_axes = [plt.axes([0.2, 0.42 - i*0.05, 0.6, 0.03]) for i in range(6)]

        self.sliders = [
            Slider(slider_axes[0], 'q1', -90, 90, valinit=0),
            Slider(slider_axes[1], 'q2', -90, 90, valinit=0),
            Slider(slider_axes[2], 'q3', -90, 90, valinit=0),
            Slider(slider_axes[3], 'q4', -90, 90, valinit=0),
            Slider(slider_axes[4], 'q5', -90, 90, valinit=0),
            Slider(slider_axes[5], 'q6', -90, 90, valinit=0),
        ]

        for slider in self.sliders:
            slider.on_changed(self.update)

        resetax = plt.axes([0.8, 0.02, 0.1, 0.04])
        button = Button(resetax, 'Reset', color='white', hovercolor='0.975')
        button.on_clicked(self.reset)

        plt.subplots_adjust(left=0.1, bottom=0.05, top=0.95)
        plt.show()

    def update(self, val):
        self.q = [s.val for s in self.sliders]
        self.get_pose_to_origin_pose()
        self.draw_axes_tf(self.poses)

    def reset(self, event):
        for slider in self.sliders:
            slider.reset()

if __name__ == "__main__":
    robot = PoseViewer()
    robot.slider()
