import requests
from PIL import Image
from io import BytesIO
import os

def generar_matriz_desde_imagen(url_imagen):
    # Descargar la imagen desde la URL
    respuesta = requests.get(url_imagen)
    
    # Verificar si la descarga fue exitosa
    if respuesta.status_code == 200:
        # Abrir la imagen desde los datos descargados
        imagen = Image.open(BytesIO(respuesta.content))
        
        # Redimensionar la imagen para hacerla más pequeña
        ancho_nuevo = 100  # Cambia este valor según el tamaño deseado
        alto_nuevo = int(imagen.height * (ancho_nuevo / imagen.width))
        imagen = imagen.resize((ancho_nuevo, alto_nuevo))
        
        # Obtener las dimensiones de la imagen
        ancho, alto = imagen.size
        
        # Crear una matriz para almacenar los valores de profundidad y color
        matriz = []
        
        # Obtener los valores de profundidad y color de cada punto y almacenarlos en la matriz
        for y in range(alto):
            fila = []
            for x in range(ancho):
                # Obtener el color RGB del punto en la posición (x, y)
                pixel = imagen.getpixel((x, y))
                # Calcular la profundidad como la escala de grises ponderada
                profundidad = int(0.2126 * pixel[0] + 0.7152 * pixel[1] + 0.0722 * pixel[2])
                # Convertir el color RGB en un valor hexadecimal sin el símbolo "#"
                color_hex = '{:02x}{:02x}{:02x}'.format(pixel[0], pixel[1], pixel[2])
                # Agregar el par profundidad-color a la fila
                fila.append((profundidad, color_hex))
            # Agregar la fila a la matriz
            matriz.append(fila)
        
        return matriz
    else:
        print("Error al descargar la imagen")
        return None

def guardar_en_fdf(matriz, nombre_archivo):
    with open(nombre_archivo, "w") as archivo:
        for fila in matriz:
            fila_str = ""
            for punto in fila:
                # Concatenar la profundidad y el color en formato hexadecimal
                fila_str += "{},0x{} ".format(punto[0], punto[1])
            # Escribir la fila en el archivo, eliminando el espacio final
            archivo.write(fila_str[:-1] + "\n")

# URL de la imagen
url_imagen = "https://www3.gobiernodecanarias.org/medusa/ecoblog/mrodperv/files/2015/12/f.jpg"

# Nombre del archivo FDF
nombre_archivo = "map.fdf"

# Generar la matriz de profundidad y color desde la imagen
matriz = generar_matriz_desde_imagen(url_imagen)

if matriz is not None:
    # Verificar si el archivo ya existe
    if os.path.exists(nombre_archivo):
        print("El archivo", nombre_archivo, "ya existe. Sobrescribiendo...")
    
    # Guardar la matriz en un archivo FDF (modo "w" sobrescribe el archivo existente)
    guardar_en_fdf(matriz, nombre_archivo)
    print("Archivo guardado exitosamente como", nombre_archivo)
