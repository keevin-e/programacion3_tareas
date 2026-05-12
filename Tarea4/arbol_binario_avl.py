from nodo import nodo
from graphviz_class import graphviz_class
import csv

# ============================================
# CLASE BASE: ÁRBOL BINARIO DE BÚSQUEDA (ABB)
# ============================================

class arbolBinario:
    """Clase base para Árbol Binario de Búsqueda sin balanceo"""
    
    def __init__(self):
        self.raiz = None
        self.grafica = graphviz_class()
    
    def actualizar_grafica(self):
        """Actualiza la visualización del árbol"""
        self.grafica.limpiar()
        if self.raiz is not None:
            self.grafica.adicion_nodo(self.raiz.valor)
        self.recorrer_arbol(self.raiz)
        self.grafica.guardar(abrir=False)
        
    def recorrer_arbol(self, nodo_actual):
        """Recorre el árbol para agregar nodos a la gráfica"""
        if nodo_actual is not None:
            if nodo_actual.izquierda is not None:
                self.grafica.adicion_nodo(nodo_actual.izquierda.valor, nodo_actual.valor, 'izquierda')
                self.recorrer_arbol(nodo_actual.izquierda)
            if nodo_actual.derecha is not None:
                self.grafica.adicion_nodo(nodo_actual.derecha.valor, nodo_actual.valor, 'derecha')
                self.recorrer_arbol(nodo_actual.derecha)

    def encontrar_minimo(self, nodo_actual):
        """Encuentra el nodo con valor mínimo en un subárbol"""
        actual = nodo_actual
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    def insertar(self, valor):
        """Inserta un nuevo nodo en el árbol"""
        self.raiz = self.insertar_recursivo(self.raiz, valor)
        self.actualizar_grafica()

    def insertar_recursivo(self, nodo_actual, valor):
        """Inserción ABB simple (sin balanceo)"""
        if nodo_actual is None:
            return nodo(valor)
        if valor < nodo_actual.valor:
            nodo_actual.izquierda = self.insertar_recursivo(nodo_actual.izquierda, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecha = self.insertar_recursivo(nodo_actual.derecha, valor)
        return nodo_actual
    
    def buscar(self, valor):
        """Busca un valor en el árbol"""
        return self.buscar_recursivo(self.raiz, valor)
    
    def buscar_recursivo(self, nodo_actual, valor):
        """Búsqueda recursiva ABB"""
        if nodo_actual is None:
            return False
        if nodo_actual.valor == valor: 
            return True
        elif valor < nodo_actual.valor:
            return self.buscar_recursivo(nodo_actual.izquierda, valor)
        else:
            return self.buscar_recursivo(nodo_actual.derecha, valor) 

    def eliminar(self, valor):
        """Elimina un nodo del árbol"""
        self.raiz = self.eliminar_recursivo(self.raiz, valor)
        self.actualizar_grafica()

    def eliminar_recursivo(self, nodo_actual, valor):
        """Eliminación ABB simple (sin balanceo)"""
        if nodo_actual is None:
            return nodo_actual
        if valor < nodo_actual.valor:
            nodo_actual.izquierda = self.eliminar_recursivo(nodo_actual.izquierda, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecha = self.eliminar_recursivo(nodo_actual.derecha, valor)
        else:
            if nodo_actual.izquierda is None:
                return nodo_actual.derecha
            elif nodo_actual.derecha is None:
                return nodo_actual.izquierda
            temp = self.encontrar_minimo(nodo_actual.derecha)
            nodo_actual.valor = temp.valor
            nodo_actual.derecha = self.eliminar_recursivo(nodo_actual.derecha, temp.valor)
        return nodo_actual
    
    def cargar_desde_csv(self, nombre_archivo):
        """Carga valores desde archivo CSV"""
        with open(nombre_archivo, 'r') as archivo:
            lector_csv = csv.reader(archivo)
            for fila in lector_csv:
                for valor in fila:
                    self.insertar(int(valor))


# ============================================
# CLASE DERIVADA: ÁRBOL AVL (CON HERENCIA)
# ============================================

class arbolAVL(arbolBinario):
    """Árbol Binario AVL - hereda de arbolBinario y agrega balanceo"""
    
    # --- Métodos AVL: Altura y Balance ---
    
    def get_altura(self, nodo_actual):
        """Obtiene la altura de un nodo"""
        if nodo_actual is None:
            return 0
        return nodo_actual.altura

    def actualizar_altura(self, nodo_actual):
        """Actualiza la altura de un nodo"""
        nodo_actual.altura = 1 + max(
            self.get_altura(nodo_actual.izquierda),
            self.get_altura(nodo_actual.derecha)
        )

    def get_balance(self, nodo_actual):
        """Obtiene el factor de balance de un nodo"""
        if nodo_actual is None:
            return 0
        return self.get_altura(nodo_actual.izquierda) - self.get_altura(nodo_actual.derecha)

    # --- Rotaciones AVL ---
    
    def rotar_derecha(self, padre): 
        """Rotación a la derecha: pivot sube y padre baja"""
        pivot = padre.izquierda       # Nodo que SUBE
        subarbol = pivot.derecha      # Lo que se mueve
        pivot.derecha = padre         # pivot SUBE
        padre.izquierda = subarbol    # padre BAJA
        self.actualizar_altura(padre)
        self.actualizar_altura(pivot)
        return pivot

    def rotar_izquierda(self, padre):
        """Rotación a la izquierda: pivot sube y padre baja"""
        pivot = padre.derecha         # Nodo que SUBE
        subarbol = pivot.izquierda    # Lo que se mueve
        pivot.izquierda = padre       # pivot SUBE
        padre.derecha = subarbol      # padre BAJA
        self.actualizar_altura(padre)
        self.actualizar_altura(pivot)
        return pivot

    # --- Sobrescribe los métodos de inserción y eliminación con rebalanceo AVL ---
    
    def insertar_recursivo(self, nodo_actual, valor):
        """OVERRIDE: Inserción con rebalanceo AVL"""
        if nodo_actual is None:
            return nodo(valor)
        if valor < nodo_actual.valor:
            nodo_actual.izquierda = self.insertar_recursivo(nodo_actual.izquierda, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecha = self.insertar_recursivo(nodo_actual.derecha, valor)
        else:
            return nodo_actual  # Valores duplicados no se insertan

        self.actualizar_altura(nodo_actual)
        balance = self.get_balance(nodo_actual)

        # Caso Izquierda-Izquierda
        if balance > 1 and valor < nodo_actual.izquierda.valor:
            return self.rotar_derecha(nodo_actual)
        # Caso Derecha-Derecha
        if balance < -1 and valor > nodo_actual.derecha.valor:
            return self.rotar_izquierda(nodo_actual)
        # Caso Izquierda-Derecha
        if balance > 1 and valor > nodo_actual.izquierda.valor:
            nodo_actual.izquierda = self.rotar_izquierda(nodo_actual.izquierda)
            return self.rotar_derecha(nodo_actual)
        # Caso Derecha-Izquierda
        if balance < -1 and valor < nodo_actual.derecha.valor:
            nodo_actual.derecha = self.rotar_derecha(nodo_actual.derecha)
            return self.rotar_izquierda(nodo_actual)

        return nodo_actual

    def eliminar_recursivo(self, nodo_actual, valor):
        """OVERRIDE: Eliminación con rebalanceo AVL"""
        if nodo_actual is None:
            return nodo_actual
        if valor < nodo_actual.valor:
            nodo_actual.izquierda = self.eliminar_recursivo(nodo_actual.izquierda, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecha = self.eliminar_recursivo(nodo_actual.derecha, valor)
        else:
            if nodo_actual.izquierda is None:
                return nodo_actual.derecha
            elif nodo_actual.derecha is None:
                return nodo_actual.izquierda
            temp = self.encontrar_minimo(nodo_actual.derecha)
            nodo_actual.valor = temp.valor
            nodo_actual.derecha = self.eliminar_recursivo(nodo_actual.derecha, temp.valor)

        self.actualizar_altura(nodo_actual)
        balance = self.get_balance(nodo_actual)

        # Caso Izquierda-Izquierda
        if balance > 1 and self.get_balance(nodo_actual.izquierda) >= 0:
            return self.rotar_derecha(nodo_actual)
        # Caso Izquierda-Derecha
        if balance > 1 and self.get_balance(nodo_actual.izquierda) < 0:
            nodo_actual.izquierda = self.rotar_izquierda(nodo_actual.izquierda)
            return self.rotar_derecha(nodo_actual)
        # Caso Derecha-Derecha
        if balance < -1 and self.get_balance(nodo_actual.derecha) <= 0:
            return self.rotar_izquierda(nodo_actual)
        # Caso Derecha-Izquierda
        if balance < -1 and self.get_balance(nodo_actual.derecha) > 0:
            nodo_actual.derecha = self.rotar_derecha(nodo_actual.derecha)
            return self.rotar_izquierda(nodo_actual)

        return nodo_actual
    
        

    

