import numpy as np
import cv2
import random
import os
import sqlite3

def generar_imagenes_y_etiquetas(num_imagenes=1000, tamano=(8, 8)):
    imagenes = []
    etiquetas = []
    
    for _ in range(num_imagenes):
        # Crear una imagen de fondo blanco
        imagen = np.ones(tamano, dtype=np.uint8) * 255
        
        # Determinar si se debe insertar un triángulo de base 5 y altura 3 píxeles
        if random.random() < 0.5:
            # Generar un triángulo en una posición aleatoria
            x, y = random.randint(0, tamano[0] - 4), random.randint(0, tamano[1] - 6)
            coords = [(x, y + 2), (x + 1, y + 1), (x + 1, y + 3), (x + 2, y), (x + 2, y + 1), (x + 2, y + 2), (x + 2, y + 3), (x + 2, y + 4)]
            for coord in coords:
                imagen[coord] = 0
            
            # Añadir píxeles negros adicionales que no toquen el triángulo
            for _ in range(random.randint(1, tamano[0] * tamano[1] - 8)):
                while True:
                    px, py = random.randint(0, tamano[0]-1), random.randint(0, tamano[1]-1)
                    if (px, py) not in coords and not (x - 1 <= px <= x + 3 and y - 1 <= py <= y + 5):
                        imagen[px, py] = 0
                        break
            
            # Verificar si hay píxeles negros fuera del triángulo adyacente
            etiqueta = "sí"
            for i in range(-1, 4):
                for j in range(-1, 6):
                    if (0 <= x + i < tamano[0] and 0 <= y + j < tamano[1]) and ((i, j) not in [(2, -1), (2, 5)] and ((i in [-1, 3] and j in range(6)) or (j in [-1, 6] and i in range(4)))):
                        if imagen[x + i, y + j] == 0:
                            etiqueta = "no"
                            break
                if etiqueta == "no":
                    break
        else:
            # Insertar píxeles negros aleatorios sin formar el triángulo
            num_pixeles_negros = random.randint(1, tamano[0] * tamano[1])
            for _ in range(num_pixeles_negros):
                x, y = random.randint(0, tamano[0]-1), random.randint(0, tamano[1]-1)
                imagen[x, y] = 0
            etiqueta = "no"
        
        imagenes.append(imagen)
        etiquetas.append(etiqueta)
    
    return imagenes, etiquetas

def guardar_imagenes_e_etiquetas(imagenes, etiquetas, carpeta="imagenes"):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    for i, (imagen, etiqueta) in enumerate(zip(imagenes, etiquetas)):
        # Guardar la imagen
        nombre_imagen = os.path.join(carpeta, f"imagen_{i+1}.png")
        cv2.imwrite(nombre_imagen, imagen)
        
        # Guardar la etiqueta
        nombre_etiqueta = os.path.join(carpeta, f"etiqueta_{i+1}.txt")
        with open(nombre_etiqueta, 'w') as f:
            f.write(etiqueta)

def crear_base_de_datos(nombre_db="imagenes.db"):
    conn = sqlite3.connect(nombre_db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imagenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_imagen TEXT,
            etiqueta TEXT
        )
    ''')
    conn.commit()
    conn.close()

def limpiar_base_de_datos(nombre_db="imagenes.db"):
    conn = sqlite3.connect(nombre_db)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM imagenes')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="imagenes"')
    conn.commit()
    conn.close()

def insertar_en_base_de_datos(imagenes, etiquetas, nombre_db="imagenes.db"):
    conn = sqlite3.connect(nombre_db)
    cursor = conn.cursor()
    
    for i, (imagen, etiqueta) in enumerate(zip(imagenes, etiquetas)):
        nombre_imagen = f"imagen_{i+1}.png"
        cursor.execute('''
            INSERT INTO imagenes (nombre_imagen, etiqueta) VALUES (?, ?)
        ''', (nombre_imagen, etiqueta))
    
    conn.commit()
    conn.close()

# Generar imágenes y etiquetas
imagenes, etiquetas = generar_imagenes_y_etiquetas()

# Guardar imágenes y etiquetas en la carpeta "imagenes"
guardar_imagenes_e_etiquetas(imagenes, etiquetas)

# Crear base de datos
crear_base_de_datos()

# Limpiar la base de datos y restablecer el ID
limpiar_base_de_datos()

# Insertar imágenes y etiquetas en la base de datos
insertar_en_base_de_datos(imagenes, etiquetas)
