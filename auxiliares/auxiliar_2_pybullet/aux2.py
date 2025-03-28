import pybullet as p
import pybullet_data
import time
import numpy as np

## --- Comandos de Configuración --- ##

# Init del simulador de Pybullet
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Init de físicas y tiempo
p.setGravity(0,0,-9.81) 
p.setRealTimeSimulation(1) 

# Carga de un entorno visual
planeId = p.loadURDF("plane.urdf")

# Carga del modelo en formato URDF, su posición y tipo de joint con el mundo
robotic_arm = p.loadURDF("auxiliares/auxiliar_2_pybullet/example_robot.urdf", basePosition=[0, 0, 0], useFixedBase=True)


## --- Caracterización del robot cargado --- ##

# Define the joint indices for each link of the robot
num_joints = p.getNumJoints(robotic_arm)
print("Este robot posee: ",num_joints, " joints")

# Marcador de links en base al número de joints.
link_indices = [joint_index for joint_index in range(num_joints)]
print(link_indices)



## --- Init de la simulación ---##

# Crear un "slider" para cada Joint (articulación)
sliders = [p.addUserDebugParameter(f"Link {i+1}", -np.pi, np.pi, 0) for i in range(num_joints)]

def move_robot():
    while True:
        # Guardar los ángulos de los "sliders"
        angles = [p.readUserDebugParameter(slider) for slider in sliders]
        print(angles) # valores en lista

        # Publicar valores de los sliders en el robot
        for i, angle in enumerate(angles):
            p.setJointMotorControl2(robotic_arm, link_indices[i], p.POSITION_CONTROL, targetPosition=angle)

        # Crear un "evento"
        p.stepSimulation()
        time.sleep(1/240)  # Tiempo entre "eventos"

# llamar la función para ejecutar el código
move_robot()


"""
Actividades (una a la vez, en el orden dado):
1. Mueve el robot de dos links con sliders
2. Mueve el robot de dos link a un punto determinado en código, sin sliders

3. Quitar el robot de dos links del simulador

4. Elige otro manipulador y agregalo al simulador
5. Agregar un objeto al simulador, dentro del espacio de trabajo del segundo robot

6. Mueve la punta del manipulador cerca del objeto usando cinematica directa
7. Mueve la punta del manipulador cerca del objeto usando cinematica inversa
"""