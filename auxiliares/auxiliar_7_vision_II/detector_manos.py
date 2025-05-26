import cv2
import mediapipe as mp

# Inicialización de cámara
dispositivoCaptura = cv2.VideoCapture(0)
dispositivoCaptura.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
dispositivoCaptura.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Configuración de MediaPipe
mpManos = mp.solutions.hands
manos = mpManos.Hands(static_image_mode=False, max_num_hands=5,
                      min_detection_confidence=0.7, min_tracking_confidence=0.7)
mpDibujar = mp.solutions.drawing_utils

while True:
    success, img = dispositivoCaptura.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resultado = manos.process(imgRGB)

    if resultado.multi_hand_landmarks:
        for handLms in resultado.multi_hand_landmarks:
            mpDibujar.draw_landmarks(img, handLms, mpManos.HAND_CONNECTIONS)

            # Calcular centro promedio (cx, cy) de los landmarks
            h, w, _ = img.shape
            suma_x = 0
            suma_y = 0
            total_puntos = len(handLms.landmark)

            for punto in handLms.landmark:
                px = int(punto.x * w)
                py = int(punto.y * h)
                suma_x += px
                suma_y += py

            cx = int(suma_x / total_puntos)
            cy = int(suma_y / total_puntos)

            # Dibujar centro en azul y escribir coordenadas
            cv2.circle(img, (cx, cy), 7, (255, 0, 0), -1)
            cv2.putText(img, f"Centro: ({cx}, {cy})", (cx - 60, cy - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            print(f"Centro Mano: x = {cx}, y = {cy}")

    else:
        print("No manos")

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

dispositivoCaptura.release()
cv2.destroyAllWindows()
