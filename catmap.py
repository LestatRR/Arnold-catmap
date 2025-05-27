#libreria para usar imagenes
from PIL import Image
#manejo de df y matrices
import numpy as np
#creacion de video
import cv2

#recibimos la imagen convertida en array con numpy
def cat_map(img_array):
    #N guarda filas y columnas de la matriz con shape
    N = img_array.shape[0]
    #creamos otra matriz de las mismas dimensiones y del mismo tipo de dato esta matriz sera la que guardara la iteracion
    temp = np.zeros_like(img_array)
    for x in range(N):
        for y in range(N):
            #uso de algoritmo
            new_x = (x + y) % N
            new_y = (x + 2 * y) % N
            #segun el algoritmo se cambian los pixeles
            temp[new_x, new_y] = img_array[x, y]
    return temp

def main():
    image_path = 'cat.png'
    img = Image.open(image_path).convert('RGB')

    #nos aseguramos que la imagen sea cuadrada de lo contrario la recortamos
    #sacamos el lado mas pequeno
    N = min(img.size)
    #recortamos 
    img = img.crop((0, 0, N, N))
    #trabajaremos con este array ya recortado
    original_array = np.array(img)
    
    #este array lo suaremos para guardar cada matriz iterada para hacer el video
    frames = []
    current = original_array.copy()
    #contador para iteraciones
    count = 0
    #agregamos la imagen original que se mostrara el principio del video
    frames.append(current.copy())

    while True:
        current = cat_map(current)
        count += 1
        print(f'Vamos en la iteracion {count}')
        #se van guardando en el video
        frames.append(current.copy())
        #cuando la imagen se iguala a la original o supera las 300 iteraciones termina su ejecucion 
        if np.array_equal(current, original_array) or count == 300:
            break
            
    #si las iteraciones superan las 300 directamente crea el video      
    if count == 300:
        print("Se alcanzaron las 300 iteraciones y se detuvo el proceso para evitar alto consumo de ram")
    else:
        print(f'Se necesitan {count} iteraciones para volver al inicio')
        height, width, _ = frames[0].shape
        video = cv2.VideoWriter('cat_catmap.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))

        for f in frames:
            bgr = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
            video.write(bgr)

        video.release()
        print('Video guardado como cat_catmap.mp4')


if __name__ == '__main__':
    main()
