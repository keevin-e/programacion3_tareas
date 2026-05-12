from nodo import Nodo
from utils import leer_csv, comparar_claves, NOT_FOUND


class ArbolAVL:
    """
    Árbol AVL con auto-balanceo (rotaciones simples y dobles).

    Complejidad garantizada en todos los casos:
      - Insertar:  O(log n)
      - Buscar:    O(log n)
      - Eliminar:  O(log n)

    La altura máxima del árbol nunca supera 1.44 * log2(n),
    por lo que la recursión no desborda la pila incluso con millones de nodos.
    """

    def __init__(self):
        self.raiz = None
        self.tamanio = 0

    # ------------------------------------------------------------------
    # Utilidades de altura y balance
    # ------------------------------------------------------------------

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))

    def _factor_balance(self, nodo):
        return self._altura(nodo.izquierda) - self._altura(nodo.derecha) if nodo else 0

    # ------------------------------------------------------------------
    # Rotaciones
    # ------------------------------------------------------------------

    def _rotar_derecha(self, padre):
        pivot = padre.izquierda
        subarbol = pivot.derecha
        pivot.derecha = padre
        padre.izquierda = subarbol
        self._actualizar_altura(padre)
        self._actualizar_altura(pivot)
        return pivot

    def _rotar_izquierda(self, padre):
        pivot = padre.derecha
        subarbol = pivot.izquierda
        pivot.izquierda = padre
        padre.derecha = subarbol
        self._actualizar_altura(padre)
        self._actualizar_altura(pivot)
        return pivot

    def _balancear(self, nodo):
        """Aplica la rotación necesaria si el factor de balance está fuera del rango [-1, 1]."""
        self._actualizar_altura(nodo)
        fb = self._factor_balance(nodo)

        # Caso LL: desbalance por la izquierda
        if fb > 1:
            if self._factor_balance(nodo.izquierda) < 0:   # Caso LR
                nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)

        # Caso RR: desbalance por la derecha
        if fb < -1:
            if self._factor_balance(nodo.derecha) > 0:     # Caso RL
                nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo)

        return nodo  # Árbol balanceado, no se requiere rotación

    # ------------------------------------------------------------------
    # Inserción
    # ------------------------------------------------------------------

    def insertar(self, clave, datos=None):
        """Inserta con balanceo automático O(log n)."""
        self.raiz, insertado = self._insertar(self.raiz, clave, datos)
        if insertado:
            self.tamanio += 1

    def _insertar(self, nodo, clave, datos):
        """Retorna (nodo_raiz, fue_insertado)."""
        if nodo is None:
            return Nodo(clave, datos), True

        cmp = comparar_claves(clave, nodo.clave)
        if cmp < 0:
            nodo.izquierda, insertado = self._insertar(nodo.izquierda, clave, datos)
        elif cmp > 0:
            nodo.derecha, insertado = self._insertar(nodo.derecha, clave, datos)
        else:
            nodo.datos = datos   # Clave duplicada: actualiza datos
            return nodo, False

        return self._balancear(nodo), insertado

    # ------------------------------------------------------------------
    # Búsqueda iterativa
    # ------------------------------------------------------------------

    def buscar(self, clave):
        """Búsqueda iterativa O(log n). Retorna datos o NOT_FOUND."""
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
    # Eliminación
    # ------------------------------------------------------------------

    def eliminar(self, clave):
        """Elimina y rebalancea O(log n). Retorna True si fue encontrado."""
        self.raiz, eliminado = self._eliminar(self.raiz, clave)
        if eliminado:
            self.tamanio -= 1
        return eliminado

    def _eliminar(self, nodo, clave):
        """Retorna (nodo_raiz, fue_eliminado)."""
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
            # Caso: sin hijo izquierdo
            if nodo.izquierda is None:
                return nodo.derecha, eliminado
            # Caso: sin hijo derecho
            if nodo.derecha is None:
                return nodo.izquierda, eliminado
            # Caso: dos hijos → sustituir por el sucesor in-order y rebalancear
            sucesor = self._minimo(nodo.derecha)
            nodo.clave = sucesor.clave
            nodo.datos = sucesor.datos
            nodo.derecha, _ = self._eliminar(nodo.derecha, sucesor.clave)

        return self._balancear(nodo), eliminado

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
