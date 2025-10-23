import cv2
import numpy as np
import math

def detectar_arucos(imagen_input):
    #Se puede entregar un path o una imagen
    if isinstance(imagen_input, str):
        imagen = cv2.imread(imagen_input, cv2.IMREAD_GRAYSCALE)
    else:
        imagen = imagen_input.copy()

    # Diccionario y detector
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
    detector = cv2.aruco.ArucoDetector(aruco_dict)
    # Detectar marcadores
    esquinas, ids, _ = detector.detectMarkers(imagen)
    resultados = []
    if ids is not None:
        for i in range(len(ids)):
            id_ = int(ids[i][0])
            pts = esquinas[i][0]
            # Calcular centro del marcador
            centro = pts.mean(axis=0)
            x_centro, y_centro = int(centro[0]), int(centro[1])
            # Calcular ángulo de orientación
            v = pts[1] - pts[0]
            angulo_rad = math.atan2(v[1], v[0])
            angulo_deg = math.degrees(angulo_rad)

            resultados.append({
                "id": id_,
                "posicion": (x_centro, y_centro),
                "orientacion_grados": angulo_deg
            })
    return resultados

def calcular_transformacion(puntos_pixeles, puntos_mm):
    # Convertir a np.array float32
    pts_pix = np.array(puntos_pixeles, dtype=np.float32)
    pts_mm = np.array(puntos_mm, dtype=np.float32)
    # Si se tiene 4 puntos, usar homografía
    if len(pts_pix) == 4:
        matriz, status = cv2.findHomography(pts_pix, pts_mm)
        return matriz
    else:
        matriz = cv2.getAffineTransform(pts_pix[:3], pts_mm[:3])
        return matriz

def convertir_pixel_a_mm(punto_pixel, matriz_transformacion):
    punto = np.array([ [punto_pixel[0], punto_pixel[1]] ], dtype=np.float32)
    if matriz_transformacion.shape == (3, 3):  # Homografía
        punto_homog = cv2.perspectiveTransform(np.array([punto]), matriz_transformacion)
        return tuple(punto_homog[0][0])
    else:  # Afín
        punto_af = cv2.transform(np.array([punto]), matriz_transformacion)
        return tuple(punto_af[0][0])



img = cv2.imread("foto.jpg", cv2.IMREAD_GRAYSCALE)

detecciones = detectar_arucos(img)

for d in detecciones:
    print(f"ID: {d['id']}, Posición: {d['posicion']}, Orientación: {d['orientacion_grados']:.2f}°")
posiciones_reales_mm = {
 3: (12, 25),
 9: (12, 15),
 15: (-12, 15),
 6: (-12, 25)
}

print("holaaaa")

# Filtrar las posiciones de IDs que tienes posiciones reales definidas
puntos_pixeles = []
puntos_mm = []
for d in detecciones:
    id_ = d['id']
    if id_ in posiciones_reales_mm:
        print("hola")
        puntos_pixeles.append(d['posicion'])
        puntos_mm.append(posiciones_reales_mm[id_])
# Calcular matriz de transformación píxeles -> mm
matriz_transformacion = calcular_transformacion(puntos_pixeles, puntos_mm)
# Ahora convierte un punto cualquiera (por ejemplo (350, 250) px)
punto_pixel = (210, 200)
punto_mm = convertir_pixel_a_mm(punto_pixel, matriz_transformacion)
print(f"El punto {punto_pixel} en píxeles corresponde a {punto_mm} en mm")



