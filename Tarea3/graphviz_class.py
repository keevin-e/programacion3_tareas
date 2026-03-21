import graphviz as gp

class graphviz_class:
    def __init__(self):
        self.g = gp.Digraph('G', filename='grafica.gv', format='png')
        self.g.attr(rankdir='LR')
    
    def limpiar(self):
        self.g = gp.Digraph('G', filename='grafica.gv', format='png')
        self.g.attr(rankdir='LR')
        self.nodos.clear()
    
    #funcion para agregar un nodo a la grafica, recibe el valor del nodo como parametro, dependiendo si es izquierda o derecha se agrega una conexion con el nodo padre
    def adicion_nodo(self, nodo, padre=None, posicion=None):
        """
        Agrega un nodo a la gráfica.
        
        Args:
            nodo: Valor del nodo
            padre: Nodo padre (opcional)
            posicion: 'izquierda' o 'derecha' (opcional)
        """
        if nodo not in self.nodos:
            self.g.node(str(nodo))
            self.nodos.add(nodo)
        
        # Si hay padre, validar posición y crear conexión
        if padre is not None and posicion is not None:
            if posicion.lower() not in ['izquierda', 'derecha']:
                raise ValueError("La posición debe ser 'izquierda' o 'derecha'")
            self.adicion_conexion(padre, nodo)
        
    def adicion_conexion(self, nodo1, nodo2):
        self.g.edge(str(nodo1), str(nodo2))
        
    def guardar(self, abrir=False):
        self.g.render(view=abrir)