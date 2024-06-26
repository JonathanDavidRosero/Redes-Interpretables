import numpy as np
import cv2
import random
import os
import sqlite3

def generar_imagenes_y_etiquetas(num_imagenes=1000, tamano=(5, 5)):
    imagenes = []
    etiquetas = []
    
    for _ in range(num_imagenes):
        # Crear una imagen de fondo blanco
        imagen = np.ones(tamano, dtype=np.uint8) * 255
        
        # Insertar píxeles negros aleatorios
        num_pixeles_negros = random.randint(1, tamano[0] * tamano[1])
        for _ in range(num_pixeles_negros):
            x, y = random.randint(0, tamano[0]-1), random.randint(0, tamano[1]-1)
            imagen[x, y] = 0
        
        # Asignar la etiqueta según el píxel en la esquina superior izquierda
        etiqueta = "sí" if imagen[0, 0] == 0 else "no"
        
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
