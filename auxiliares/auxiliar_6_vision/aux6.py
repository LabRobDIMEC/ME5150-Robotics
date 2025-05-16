import cv2
import numpy as np

######### LEER IMAGEN #########
def read_img(path, mode='rgb'):
    if mode == 'gray':
        imagen = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    elif mode == 'rgb':
        imagen = cv2.imread(path, cv2.IMREAD_COLOR)
    else:
        imagen = cv2.imread(path)  

    return imagen

def show_img(img,title):
    cv2.imshow(title,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
show_img(read_img("lena.jpg",mode="gray"),"gray image")
show_img(read_img("chess_board.jpg",mode="rgb"),"rgb image")


####### Operacion punto a punto ###########
def agregar_brillo(img, brillo):

    n,m = img.shape

    for i in range(n):
        for j in range(m):
            valor = img[i,j] + brillo
            if valor > 255:
                valor = 255
            elif valor <0:
                valor = 0

            img[i,j] = valor

    return img

img = read_img("lena.jpg",mode="gray")
show_img( img ,"gray image")
show_img(agregar_brillo(img,-50),"brillo ajustado")


def umbralizacion (img,umbral):
    n,m = img.shape
    for i in range(n):
        for j in range(m):
            if img[i,j] < umbral:
                img[i,j] = 0
    
    return img

show_img(umbralizacion(img,100),"umbralizado")

####### Convolución ##############

def convolucion(img, kernel):
    resultado = cv2.filter2D(img, -1, kernel)

    return resultado

kernel = np.array([[-1, -1, -1],
                    [-1,  8, -1],
                    [-1, -1, -1]])

img = read_img("chess_board.jpg",mode="gray")

show_img(convolucion(img,kernel),"convolucion")

####### Filtrado #########

def filtrar(img, tipo="bajo"):
    if tipo == "bajo":
        # Filtro pasa bajo: Gaussiano
        resultado = cv2.GaussianBlur(img, (5, 5), 0)
    elif tipo == "alto":
        # Filtro pasa alto: detección de bordes con Canny
        resultado = cv2.Canny(img, 100, 200)
    else:
        raise ValueError("Tipo debe ser 'bajo' (Gaussiano) o 'alto' (Canny)")

    return resultado

show_img(filtrar(img,tipo="alto"),"filtrado")

