import graphviz as gp


class graphviz_class:
    def __init__(self):
        # crear el grafo dirigido y dirección
        self.g = gp.Digraph('G', filename='grafica.gv', format='png')
        self.g.attr(rankdir='TB')
        self.g.attr('node', shape='record', fontsize='11')

    def limpiar(self):
        # reinicia el grafo para generar una representación fresca del árbol
        # se llama antes de cada actualización para no acumular nodos anteriores
        self.g = gp.Digraph('G', filename='grafica.gv', format='png')
        self.g.attr(rankdir='TB')
        self.g.attr('node', shape='record', fontsize='11')

    def adicion_nodo(self, node_id, claves):
        # agrega un nodo al grafo con sus claves mostradas en celdas horizontales
        parts = ['<f0>']
        for i, clave in enumerate(claves):
            parts.append(f' {clave} ')
            parts.append(f'<f{i + 1}>')
        label = '|'.join(parts) + ' '   # espacio final: fuerza comillas en el DOT
        self.g.node(node_id, label=label)

    def adicion_conexion(self, padre_id, hijo_id, puerto_idx):
        # dibuja una arista desde el puerto f{puerto_idx} del nodo padre
        # hasta el nodo hijo, reflejando qué ranura del padre apunta a cada hijo
        self.g.edge(f'{padre_id}:f{puerto_idx}', hijo_id)

    def guardar(self, abrir=False):
        # renderiza el grafo y lo guarda como grafica.gv y grafica.gv.png
        # con abrir=True se abre automáticamente la imagen al terminar
        self.g.render(view=abrir)
