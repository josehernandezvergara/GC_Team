import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation

def animar_simulacion(model, estados, velocidad_ms=50):
    height, width = model.forest.shape
    fig, ax = plt.subplots(figsize=(8,8))
    cmap = mcolors.ListedColormap(['green', 'red', 'black', 'white'])
    bounds = [-1, 0, 1, 2, 3]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    im = ax.imshow(estados[0], cmap=cmap, norm=norm)
    plt.title('animacion de propagacion del fuego')
    plt.xlabel('columna')
    plt.ylabel('fila')
    plt.colorbar(im, ticks=[-1,0,1,2], label='-1: sin arbol, 0: vivo, 1: quemando, 2: quemado')
    def update(frame):
        im.set_data(estados[frame])
        ax.set_title(f'paso {frame+1} / {len(estados)}')
        return [im]
    ani = animation.FuncAnimation(fig, update, frames=len(estados), interval=velocidad_ms, blit=False, repeat=False)
    plt.show()
