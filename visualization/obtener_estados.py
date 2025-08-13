import numpy as np

def obtener_estados(model, max_pasos=None):
    height, width = model.forest.shape
    estados = []
    pasos = 0
    while True:
        if max_pasos is not None and pasos >= max_pasos:
            print(f"se alcanzo el tope de pasos: {max_pasos}. STOP.")
            model.running = False
            break
        estado = np.full((height, width), -1)
        for arbol in model.agents:
            fila, col = model.forest.positions[arbol]
            estado[fila, col] = arbol.condition
        estados.append(estado.copy())
        pasos += 1
        if not model.running:
            break
        model.step()
    return estados
