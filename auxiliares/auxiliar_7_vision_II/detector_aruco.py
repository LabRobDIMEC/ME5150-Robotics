import cv2
import cv2.aruco as aruco

# Lista de diccionarios ArUco a probar
aruco_dicts = {
    "DICT_4X4_50": aruco.DICT_4X4_50,
    "DICT_5X5_100": aruco.DICT_5X5_100,
    "DICT_6X6_250": aruco.DICT_6X6_250,
    "DICT_7X7_1000": aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": aruco.DICT_ARUCO_ORIGINAL
}

# Preparar detectores para cada diccionario
detectors = {}
for name, dict_id in aruco_dicts.items():
    dictionary = aruco.getPredefinedDictionary(dict_id)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(dictionary, parameters)
    detectors[name] = (dictionary, detector)

# Captura de video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()

print("Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for dict_name, (dictionary, detector) in detectors.items():
        corners, ids, _ = detector.detectMarkers(gray)
        if ids is not None:
            aruco.drawDetectedMarkers(frame, corners, ids)
            for i, marker_id in enumerate(ids):
                print(f"[{dict_name}] ID detectado: {marker_id[0]}")

    cv2.imshow("Detección ArUco Múltiple", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()