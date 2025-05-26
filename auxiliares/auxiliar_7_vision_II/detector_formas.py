import cv2
import numpy as np


def umbral(img,rojo=0,azul=0,verde=0):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Crear máscara donde TODOS los canales sean mayores al umbral
    mascara = cv2.inRange(img, (rojo, azul,verde), (255, 255, 255))
    # Aplicar la máscara
    resultado = cv2.bitwise_and(img, img, mask=mascara)

    return cv2.cvtColor(resultado, cv2.COLOR_RGB2BGR)


# Cargar imagen
img = cv2.imread("auxiliares/auxiliar_7_vision_II/formas_regulares.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Filtro pasa bajo (suavizado)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Filtro pasa alto (realzado de bordes)
laplacian = cv2.Laplacian(blur, cv2.CV_64F)
laplacian = cv2.convertScaleAbs(laplacian)

# Detección de bordes
edges = cv2.Canny(laplacian, 50, 150)
img_rojo = umbral(img,rojo=240)


cv2.imshow("Detección de Figuras", img_rojo)
cv2.waitKey(0)


imgGris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, imgBinaria = cv2.threshold(edges, 150, 255, cv2.THRESH_BINARY_INV)

# Encontrar contornos
contornos, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contorno in contornos:
    # Calcular perímetro
    perimetro = cv2.arcLength(contorno, True)
    # Aproximar a una figura poligonal
    approx = cv2.approxPolyDP(contorno, 0.02 * perimetro, True)

    # Calcular área
    area = cv2.contourArea(contorno)

    # Centro del contorno para poner el texto
    M = cv2.moments(contorno)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = 0, 0

    # Clasificación de figura
    tipo = " "
    if len(approx) == 3:
        tipo = "Triangulo"
    elif len(approx) == 4:
        # Verificamos si es cuadrado o rectángulo
        (x, y, w, h) = cv2.boundingRect(approx)
        ratio = w / float(h)
        tipo = "Cuadrado" if 0.95 < ratio < 1.05 else "Rectangulo"
    elif len(approx) > 4:
        # Verificamos circularidad: 4πA / P² ~ 1 si es círculo
        circularidad = (4 * np.pi * area) / (perimetro * perimetro)
        if circularidad > 0.8:
            tipo = "Circulo"

    # Dibujar contorno
    cv2.drawContours(img, [contorno], -1, (0, 255, 0), 2)
    # Escribir tipo
    cv2.putText(img, tipo, (cx - 50, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # Centro azul
    cv2.circle(img, (cx, cy), 5, (255, 0, 0), -1)  
    #coordenada px:
    cv2.putText(img, str([cx, cy]), (cx , cy - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


# Mostrar imagen
cv2.imshow("Detección de Figuras", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
