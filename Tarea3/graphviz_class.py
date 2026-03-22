import graphviz as gp

class graphviz_class:
    def __init__(self):
        self.g = gp.Digraph('G', filename='grafica.gv', format='png')
        self.g.attr(rankdir='TB')
    
    def limpiar(self):
        self.g = gp.Digraph('G', filename='grafica.gv', format='png')
        self.g.attr(rankdir='TB')
    
    
    def adicion_nodo(self, nodo, padre=None, posicion=None):
        if padre is None:
            self.g.node(str(nodo))

        if padre is not None and posicion is not None:
            self.adicion_conexion(padre, nodo, posicion.lower())
            
    #funcion para agregar un nodo a la grafica, recibe el valor del nodo como parametro, dependiendo si es izquierda o derecha se agrega una conexion con el nodo padre    
    def adicion_conexion(self, nodo1, nodo2, posicion=None):
        if posicion == 'izquierda':
            self.g.edge(str(nodo1), str(nodo2), tailport='sw', headport='n')
        elif posicion == 'derecha':
            self.g.edge(str(nodo1), str(nodo2), tailport='se', headport='n')
        else:
            self.g.edge(str(nodo1), str(nodo2))
        
    def guardar(self, abrir=False):
        self.g.render(view=abrir)