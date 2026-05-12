class Nodo:
    """
    Nodo genérico compatible con Lista Simple, ABB y AVL.
    Almacena una clave de comparación y un dict con todos los campos del registro.
    """
    def __init__(self, clave, datos=None):
        self.clave = clave       # Clave de comparación (str o float)
        self.datos = datos       # Dict con todos los campos del CSV

        # Punteros para Lista Simple
        self.siguiente = None

        # Punteros para árboles (ABB y AVL)
        self.izquierda = None
        self.derecha = None
        self.altura = 1          # Altura del nodo (usada exclusivamente por AVL)
