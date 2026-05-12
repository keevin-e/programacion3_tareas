from nodo import Nodo
from utils import leer_csv, comparar_claves, NOT_FOUND


class ArbolBinario:
    """
    Árbol Binario de Búsqueda (ABB) sin balanceo automático.

    Complejidad (promedio con datos aleatorios):
      - Insertar:  O(log n) promedio — O(n) peor caso (datos ordenados)
      - Buscar:    O(log n) promedio — O(n) peor caso
      - Eliminar:  O(log n) promedio — O(n) peor caso

    Inserción y búsqueda son iterativas para evitar desbordamiento de pila
    con datasets muy grandes.
    """

    def __init__(self):
        self.raiz = None
        self.tamanio = 0

    # ------------------------------------------------------------------
    # Inserción iterativa
    # ------------------------------------------------------------------

    def insertar(self, clave, datos=None):
        """Inserta un nodo de forma iterativa. Si la clave ya existe, actualiza los datos."""
        if self.raiz is None:
            self.raiz = Nodo(clave, datos)
            self.tamanio += 1
            return
        actual = self.raiz
        while True:
            cmp = comparar_claves(clave, actual.clave)
            if cmp < 0:
                if actual.izquierda is None:
                    actual.izquierda = Nodo(clave, datos)
                    self.tamanio += 1
                    return
                actual = actual.izquierda
            elif cmp > 0:
                if actual.derecha is None:
                    actual.derecha = Nodo(clave, datos)
                    self.tamanio += 1
                    return
                actual = actual.derecha
            else:
                actual.datos = datos  # Clave duplicada: actualiza datos
                return

    # ------------------------------------------------------------------
    # Búsqueda iterativa
    # ------------------------------------------------------------------

    def buscar(self, clave):
        """Busca la clave de forma iterativa. Retorna los datos o NOT_FOUND."""
        actual = self.raiz
        while actual is not None:
            cmp = comparar_claves(clave, actual.clave)
            if cmp == 0:
                return actual.datos
            elif cmp < 0:
                actual = actual.izquierda
            else:
                actual = actual.derecha
        return NOT_FOUND

    # ------------------------------------------------------------------
    # Eliminación recursiva
    # ------------------------------------------------------------------

    def eliminar(self, clave):
        """Elimina el nodo con la clave dada. Retorna True si fue encontrado."""
        self.raiz, eliminado = self._eliminar(self.raiz, clave)
        if eliminado:
            self.tamanio -= 1
        return eliminado

    def _eliminar(self, nodo, clave):
        if nodo is None:
            return None, False
        cmp = comparar_claves(clave, nodo.clave)
        eliminado = False
        if cmp < 0:
            nodo.izquierda, eliminado = self._eliminar(nodo.izquierda, clave)
        elif cmp > 0:
            nodo.derecha, eliminado = self._eliminar(nodo.derecha, clave)
        else:
            eliminado = True
            # Caso 1: sin hijo izquierdo
            if nodo.izquierda is None:
                return nodo.derecha, eliminado
            # Caso 2: sin hijo derecho
            if nodo.derecha is None:
                return nodo.izquierda, eliminado
            # Caso 3: dos hijos → sustituir por el sucesor in-order
            sucesor = self._minimo(nodo.derecha)
            nodo.clave = sucesor.clave
            nodo.datos = sucesor.datos
            nodo.derecha, _ = self._eliminar(nodo.derecha, sucesor.clave)
        return nodo, eliminado

    def _minimo(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

    # ------------------------------------------------------------------
    # Carga masiva desde CSV
    # ------------------------------------------------------------------

    def cargar_desde_csv(self, archivo, columna_clave, convertir_numero=True):
        """
        Carga registros desde un CSV usando 'columna_clave' como clave de comparación.
        Retorna (insertados, errores).
        """
        registros, errores = leer_csv(archivo, columna_clave, convertir_numero)
        for clave, fila in registros:
            self.insertar(clave, fila)
        return len(registros), errores
