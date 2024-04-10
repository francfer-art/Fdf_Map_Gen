from PIL import Image

def cargar_desde_fdf(nombre_archivo):
    matriz = []
    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            fila = []
            puntos = linea.strip().split(" ")
            for punto in puntos:
                profundidad, color_hex = punto.split(",")[0], punto.split(",")[1]
                # Handle the case where color_hex might start with '0x'
                if color_hex.startswith('0x'):
                    color_hex = color_hex[2:]
                fila.append((int(profundidad), tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4, 6))))
            matriz.append(fila)
    return matriz

def generar_imagen_desde_matriz(matriz):
    ancho = len(matriz[0])
    alto = len(matriz)
    imagen = Image.new("RGBA", (ancho, alto))
    for y in range(alto):
        for x in range(ancho):
            profundidad, color = matriz[y][x]
            imagen.putpixel((x, y), color)
    return imagen

# Nombre del archivo FDF
nombre_archivo = "map.fdf"

# Cargar la matriz desde el archivo FDF
matriz = cargar_desde_fdf(nombre_archivo)

# Generar la imagen desde la matriz
imagen = generar_imagen_desde_matriz(matriz)

# Guardar la imagen generada
nombre_imagen = "generated_map.png"
imagen.save(nombre_imagen)

print(f"Imagen generada exitosamente como {nombre_imagen}")
