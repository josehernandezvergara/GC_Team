def diagnostico_inicial(mascara):
    total = mascara.size
    arboles = mascara.sum()
    print(f"total de celdas: {total}")
    print(f"celdas con arbol: {arboles}")
    print(f"celdas vacias: {total-arboles}")
