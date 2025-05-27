#libreria para el manejo de imagenes
from PIL import Image
#clasico para el manejo de df y matrices
import numpy as np
#lo usamos para crear el video
import cv2

#cada que llamamos esta funcion revuelve una vez la imagen hace una iteracion
#recibimos la imagen convertida en array con numpy
def cat_map(img_array):
    #N guarda filas y columnas de la matriz con shape
    N = img_array.shape[0]
    #creamos otra matriz de las mismas dimensiones y del mismo tipo de dato esta matriz sera la que guardara la iteracion
    temp = np.zeros_like(img_array)
    for x in range(N):
        for y in range(N):
            #en esta parte usamos el algoritmo 
            new_x = (x + y) % N
            new_y = (x + 2 * y) % N
            #mandamos el pixel a el lugar segun la formula
            temp[new_x, new_y] = img_array[x, y]
    return temp

def main():
    #abrimos la imagen y la convertimos exactamente a rojo verda y azul
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
    #tiene la imagen que ira cambiando
    current = original_array.copy()
    #contador para las iteraciones
    count = 0
    #agregamos la imagen original que se mostrara el principio del video
    frames.append(current.copy())

    #ahora si vamos a iterar a lo desgraciado
    while True:
        #cada iteracion current guarda una imagen distinta
        current = cat_map(current)
        count += 1
        print(f'Vamos en la iteracion {count}')
        #la vamos guardando para el video
        frames.append(current.copy())
        #si la imagen actual es igual a la imagen original salimos del while (o que las iteraciones sean mas de 300 para evitar que truene la pc)
        if np.array_equal(current, original_array) or count == 300:
            break
            
    #si las iteraciones fueron muchas entonces diretamente ya salta lo del el video        
    if count == 300:
        print("Se alcanzaron las 300 iteraciones y se detuvo el proceso para evitar alto consumo de ram")
    else:
        print(f'Se necesitan {count} iteraciones para volver al inicio')
        #apartir de aqui solo crea el video agregando frame a frame al mp4
        height, width, _ = frames[0].shape
        video = cv2.VideoWriter('cat_catmap.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))

        for f in frames:
            bgr = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
            video.write(bgr)

        video.release()
        print('Video guardado como cat_catmap.mp4')


if __name__ == '__main__':
    main()