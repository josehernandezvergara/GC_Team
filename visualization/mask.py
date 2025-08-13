import matplotlib.pyplot as plt

def mostrar_mascara(mask):
    plt.imshow(mask, cmap='gray')
    plt.title('mascara binaria de arboles')
    plt.show()
