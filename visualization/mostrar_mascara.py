import matplotlib.pyplot as plt

def mostrar_mascara(mascara):
    plt.imshow(mascara, cmap='Greens')
    plt.title('mascara de bosque (1=arbol, 0=vacío)')
    plt.show()
