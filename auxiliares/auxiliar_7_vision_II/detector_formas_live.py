import cv2
import numpy as np

def umbral(img, rojo=0, azul=0, verde=0):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mascara = cv2.inRange(img, (rojo, azul, verde), (255, 255, 255))
    resultado = cv2.bitwise_and(img, img, mask=mascara)
    return cv2.cvtColor(resultado, cv2.COLOR_RGB2BGR)

# Inicializar captura de video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

while True:
    ret, img = cap.read()
    if not ret:
        print("Error: No se pudo leer el frame.")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    laplacian = cv2.Laplacian(blur, cv2.CV_64F)
    laplacian = cv2.convertScaleAbs(laplacian)
    edges = cv2.Canny(laplacian, 50, 150)
    img_rojo = umbral(img, rojo=240)
    img_figuras = img.copy()

    _, imgBinaria = cv2.threshold(edges, 150, 255, cv2.THRESH_BINARY_INV)
    contornos, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contorno in contornos:
        perimetro = cv2.arcLength(contorno, True)
        approx = cv2.approxPolyDP(contorno, 0.02 * perimetro, True)
        area = cv2.contourArea(contorno)

        if area < 500:
            continue  # Ignorar figuras pequeñas o ruido

        tipo = None

        if len(approx) == 3:
            tipo = "Triangulo"
        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ratio = w / float(h)
            if 0.95 < ratio < 1.05:
                tipo = "Cuadrado"
            else:
                continue
        elif len(approx) > 4:
            circularidad = (4 * np.pi * area) / (perimetro * perimetro)
            if circularidad > 0.85:
                tipo = "Circulo"
            else:
                continue

        # Solo si es figura regular calculamos el centro de masa
        M = cv2.moments(contorno)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            continue

        # Dibujo y anotaciones
        cv2.drawContours(img_figuras, [contorno], -1, (0, 255, 0), 2)
        cv2.circle(img_figuras, (cx, cy), 7, (255, 0, 0), -1)  # Centro en azul
        cv2.putText(img_figuras, tipo, (cx - 40, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(img_figuras, f"CM: [{cx}, {cy}]", (cx - 50, cy + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # Mostrar resultados
    cv2.imshow("Figuras Regulares", img_figuras)
    cv2.imshow("Filtro Rojo", img_rojo)
    cv2.imshow("Bordes", edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
