from nodo import Nodo
from utils import leer_csv, NOT_FOUND


class ListaSimple:
    """
    Lista simplemente enlazada con inserción al inicio.

    Complejidad:
      - Insertar:  O(1)
      - Buscar:    O(n)  — búsqueda lineal
      - Eliminar:  O(n)  — recorre hasta encontrar la clave
    """

    def __init__(self):
        self.inicio = None
        self.tamanio = 0

    # ------------------------------------------------------------------
    # Operaciones principales
    # ------------------------------------------------------------------

    def insertar(self, clave, datos=None):
        """Inserta al inicio de la lista en O(1)."""
        nuevo = Nodo(clave, datos)
        nuevo.siguiente = self.inicio
        self.inicio = nuevo
        self.tamanio += 1

    def buscar(self, clave):
        """Recorre la lista hasta encontrar la clave. Retorna los datos o NOT_FOUND."""
        actual = self.inicio
        while actual is not None:
            if actual.clave == clave:
                return actual.datos
            actual = actual.siguiente
        return NOT_FOUND

    def eliminar(self, clave):
        """Elimina el primer nodo que coincida con la clave. Retorna True/False."""
        if self.inicio is None:
            return False
        if self.inicio.clave == clave:
            self.inicio = self.inicio.siguiente
            self.tamanio -= 1
            return True
        actual = self.inicio
        while actual.siguiente is not None:
            if actual.siguiente.clave == clave:
                actual.siguiente = actual.siguiente.siguiente
                self.tamanio -= 1
                return True
            actual = actual.siguiente
        return False

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
