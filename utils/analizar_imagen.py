import numpy as np

def analizar_imagen(ruta, mostrar_histograma=True):
    from PIL import Image
    imagen = Image.open(ruta).convert('L')
    arr = np.array(imagen)
    mask_auto = arr < 128
    # EL ARGUMENTO MOSTRAR_HISTOGRAMA SE IGNORA PARA COMPATIBILIDAD
    return arr, mask_auto, arr.min(), arr.max()
