import cv2
import numpy as np

# Cargar imagen
img = cv2.imread("formas.png")  # Reemplaza con el nombre de tu imagen
imgGris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, imgBinaria = cv2.threshold(imgGris, 127, 255, cv2.THRESH_BINARY_INV)

# Encontrar contornos
contornos, _ = cv2.findContours(imgBinaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
    tipo = "Irregular"
    if len(approx) == 3:
        tipo = "Triángulo"
    elif len(approx) == 4:
        # Verificamos si es cuadrado o rectángulo
        (x, y, w, h) = cv2.boundingRect(approx)
        ratio = w / float(h)
        tipo = "Cuadrado" if 0.95 < ratio < 1.05 else "Rectángulo"
    elif len(approx) > 4:
        # Verificamos circularidad: 4πA / P² ~ 1 si es círculo
        circularidad = (4 * np.pi * area) / (perimetro * perimetro)
        if circularidad > 0.8:
            tipo = "Círculo"

    # Dibujar contorno
    cv2.drawContours(img, [contorno], -1, (0, 255, 0), 2)
    # Escribir tipo
    cv2.putText(img, tipo, (cx - 50, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# Mostrar imagen
cv2.imshow("Detección de Figuras", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
