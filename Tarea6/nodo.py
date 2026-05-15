class nodo:
    def __init__(self, es_hoja=True):
        self.claves = []       # lista ordenada de claves almacenadas en este nodo
        self.hijos = []        # lista de referencias a los nodos hijos
                               # len(hijos) == len(claves) + 1 en nodos internos
        self.es_hoja = es_hoja # True si el nodo no tiene hijos (nivel hoja)
