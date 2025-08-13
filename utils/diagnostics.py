def diagnostico_inicial(model):
    n_burning = sum([a.condition == 1 for a in model.agents])
    print(f"arboles quemandose al inicio: {n_burning}")
    if n_burning == 0:
        print("ADVERTENCIA: ningun arbol fue marcado como quemandose. Elige otra fila o revisa la logica de inicio.")
    burning_agents = [a for a in model.agents if a.condition == 1]
    vecinos_vivos = []
    for a in burning_agents:
        vecinos = model.forest.neighbors(a)
        vivos = sum([v.condition == 0 for v in vecinos])
        vecinos_vivos.append(vivos)
    print(f"vecinos vivos de los arboles quemandose al inicio: {vecinos_vivos}")
