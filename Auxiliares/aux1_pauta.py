#Cree una funcion que pase de grados a radianes
def grad_to_rad(theta):
  return (theta*3.14)/180

#Cree una funcion que calcule la media de los numeros pares de una lista
def media_pares(lista):
  sum=0
  n=0
  for i in lista:
    if i%2 == 0:
      n+=1
      sum += i
  return sum/n


import numpy as np

# Ejemplo de una matriz 2x3 representada como una lista de listas
matriz = [
    [1, 2, 3],
    [4, 5, 6]
]

# Imprimir cada fila
for fila in matriz:
    print(fila)

#Cree una funcion que sume 2 matrices indice por indice
def sumar_matrices(matriz1, matriz2):

  matriz = np.zeros([len(matriz1),len(matriz1[0])])

  for i in range(len(matriz1)):
    for j in range(len(matriz[0])):
      matriz[i,j]=matriz1[i][j]+matriz2[i][j]

  return matriz


matriz1 = [
    [1, 2, 3],
    [4, 5, 6]
]
matriz2 = [
    [7, 8, 9],
    [10, 11, 12]
]

sumar_matrices(matriz1, matriz2)


import matplotlib.pyplot as plt

#Cree una funcion que muestre un recta entre dos puntos [x,y]
def recta(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    #Pendiente
    m = (y2 - y1) / (x2 - x1)
    # Calculamos la intersección en y (b)
    b = y1 - m * x1
    x_values = []
    y_values = []
    # 100 puntos
    for i in range(100):
        x = x1 + (x2 - x1) * (i / 99)
        y = m * x + b #Funcion de la recta
        x_values.append(x)
        y_values.append(y)

    plt.plot(x_values, y_values)
    plt.show()
    return x_values,y_values


p=recta([1,2], [3,4])


import cv2

#Defina una imagen que muestre una imagen y posteriormente muestre la imagen recortada un 10% de cada lado
def recortar_imagen(ruta_imagen):
    imagen = cv2.imread(ruta_imagen)

    alto, ancho, _ = imagen.shape

    recorte_x = int(ancho * 0.1)
    recorte_y = int(alto * 0.1)

    imagen_recortada = imagen[recorte_y:alto - recorte_y, recorte_x:ancho - recorte_x]

    cv2.imshow("imagen",imagen)
    cv2.imshow("imagen_recortada",cv2.cvtColor(imagen_recortada, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return imagen_recortada

imagen_recortada = recortar_imagen("image.jpeg")