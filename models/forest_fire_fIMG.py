import agentpy as ap
import numpy as np

class Tree(ap.Agent):
    def setup(self):
        pass

class ForestFireFIMG(ap.Model):
    def vecinos_moore(self, arbol):
        # VECINOS MOORE ROBUSTO USANDO DICCIONARIO DE POSICIONES
        # DEVUELVE LOS VECINOS MOORE (8 DIRECCIONES) QUE SON AGENTES TREE
        if not hasattr(self, '_pos2agent'):
            self._pos2agent = {self.forest.positions[a]: a for a in self.agents}
        col, fila = self.forest.positions[arbol]
        offsets = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        vecinos = []
        for dc, df in offsets:
            pos = (col+dc, fila+df)
            if pos in self._pos2agent:
                vecinos.append(self._pos2agent[pos])
        return vecinos

    def setup(self):
        from utils.analizar_imagen import analizar_imagen
        arr, mask_auto, _, _ = analizar_imagen(self.p.image_path, False)
        if self.p.threshold is not None:
            mask = arr < self.p.threshold
        else:
            mask = mask_auto
        posiciones = [(col, fila) for fila, col in zip(*np.where(mask))]
        n_arboles = len(posiciones)
        height, width = mask.shape
        self.agents = ap.AgentList(self, n_arboles, Tree)
        self.forest = ap.Grid(self, (width, height), track_empty=True)
        self.forest.add_agents(self.agents, positions=posiciones)
        for a in self.agents:
            a.condition = 0
        # BUSCA UNA FILA CON ARBOLES CONECTADOS PARA INICIAR EL INCENDIO
        fila_elegida = None
        col_central = None
        for fila in range(height):
            cols = [c for c in range(width) if mask[fila, c]]
            for i, c in enumerate(cols):
                # VERIFICA SI HAY UN ARBOL VECINO A LA DERECHA
                if (c+1) in cols:
                    fila_elegida = fila
                    col_central = c
                    break
            if fila_elegida is not None:
                break
        if fila_elegida is not None:
            # ENC
            arboles_en_fila = [a for a in self.agents if self.forest.positions[a][1] == fila_elegida]
            arbol_central = min(arboles_en_fila, key=lambda a: abs(self.forest.positions[a][0] - col_central))
            arbol_central.condition = 1
            print(f"incendio iniciado en fila {fila_elegida}, columna {self.forest.positions[arbol_central][0]}")
        else:
            print("no se encontro una fila con arboles conectados para iniciar el incendio.")
        self.t = 0  # INICIALIZAR CONTADOR DE PASOS

    def step(self):
        self._pos2agent = {self.forest.positions[a]: a for a in self.agents}
        burning_trees = self.agents.select(self.agents.condition == 1)
        print(f"paso {self.t}: {len(burning_trees)} arboles quemandose")
        nuevos_quemandose = set()
        for arbol in burning_trees:
            vecinos = self.vecinos_moore(arbol)
            for vecino in vecinos:
                if vecino.condition == 0:
                    nuevos_quemandose.add(vecino)
        print(f"  se encenderan {len(nuevos_quemandose)} nuevos arboles")
        for arbol in burning_trees:
            arbol.condition = 2
        for vecino in nuevos_quemandose:
            vecino.condition = 1
        if not self.agents.select(self.agents.condition == 1):
            print("  no quedan arboles quemandose. STOP.")
            self.stop()
        self.t += 1

    def end(self):
        quemados = len(self.agents.select(self.agents.condition == 2))
        total = len(self.agents)
        self.report('burned_pct', quemados / total if total > 0 else 0)
        self.report('num_steps', self.t)
