import cv2
import numpy as np

# Cargar imagen
img = cv2.imread("auxiliares/auxiliar_7_vision_II/formas.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Filtro pasa bajo (suavizado)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Filtro pasa alto (realzado de bordes)
laplacian = cv2.Laplacian(blur, cv2.CV_64F)
laplacian = cv2.convertScaleAbs(laplacian)

# Detección de bordes
edges = cv2.Canny(laplacian, 50, 150)

# Encontrar contornos
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar y clasificar formas
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
    if cv2.contourArea(cnt) > 100:
        if len(approx) == 3:
            shape = "Triángulo"
        elif len(approx) == 4:
            shape = "Cuadrado/Rectángulo"
        elif len(approx) > 4:
            shape = "Círculo"
        else:
            shape = "Otra"
        cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
        x, y = approx[0][0]
        cv2.putText(img, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# Mostrar resultados
cv2.imshow("Original", img)
cv2.imshow("Bordes", edges)
cv2.imshow("Pasa Alto", laplacian)
cv2.imshow("Pasa Bajo", blur)
cv2.waitKey(0)
cv2.destroyAllWindows()
