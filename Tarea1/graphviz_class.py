import graphviz as gp

class graphviz_class:
    def __init__(self):
        self.g = gp.Digraph('G', filename='grafica.gv', format='png')
        self.g.attr(rankdir='LR')
    
    def limpiar(self):
        self.g = gp.Digraph('G', filename='grafica.gv', format='png')
        self.g.attr(rankdir='LR')
    
    def adicion_nodo(self, dato):
        self.g.node(str(dato))
        
    def adicion_conexion(self, nodo1, nodo2):
        self.g.edge(str(nodo1), str(nodo2))
        
    def guardar(self, abrir=False):
        self.g.render(view=abrir)
        