# Código Base: ABB y AVL

## Nodo

```python
class nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1  # Usada por AVL
```

---

## Árbol Binario de Búsqueda (ABB)

```python
class arbolBinario:
    def __init__(self):
        self.raiz = None

    # INSERTAR
    def insertar(self, valor):
        self.raiz = self.insertar_recursivo(self.raiz, valor)

    def insertar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return nodo(valor)
        if valor < nodo_actual.valor:
            nodo_actual.izquierda = self.insertar_recursivo(nodo_actual.izquierda, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecha = self.insertar_recursivo(nodo_actual.derecha, valor)
        return nodo_actual

    # BUSCAR
    def buscar(self, valor):
        return self.buscar_recursivo(self.raiz, valor)

    def buscar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return False
        if nodo_actual.valor == valor:
            return True
        elif valor < nodo_actual.valor:
            return self.buscar_recursivo(nodo_actual.izquierda, valor)
        else:
            return self.buscar_recursivo(nodo_actual.derecha, valor)

    # ELIMINAR
    def eliminar(self, valor):
        self.raiz = self.eliminar_recursivo(self.raiz, valor)

    def eliminar_recursivo(self, nodo_actual, valor):
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
            # Dos hijos: sucesor in-order (mínimo del subárbol derecho)
            temp = self.encontrar_minimo(nodo_actual.derecha)
            nodo_actual.valor = temp.valor
            nodo_actual.derecha = self.eliminar_recursivo(nodo_actual.derecha, temp.valor)
        return nodo_actual

    def encontrar_minimo(self, nodo_actual):
        actual = nodo_actual
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual
```

---

## Árbol AVL (hereda de arbolBinario)

```python
class arbolAVL(arbolBinario):

    # ALTURA Y BALANCE
    def get_altura(self, nodo_actual):
        if nodo_actual is None:
            return 0
        return nodo_actual.altura

    def actualizar_altura(self, nodo_actual):
        nodo_actual.altura = 1 + max(
            self.get_altura(nodo_actual.izquierda),
            self.get_altura(nodo_actual.derecha)
        )

    def get_balance(self, nodo_actual):
        if nodo_actual is None:
            return 0
        return self.get_altura(nodo_actual.izquierda) - self.get_altura(nodo_actual.derecha)

    # ROTACIONES
    def rotar_derecha(self, padre):
        pivot = padre.izquierda       # pivot SUBE
        padre.izquierda = pivot.derecha
        pivot.derecha = padre         # padre BAJA
        self.actualizar_altura(padre)
        self.actualizar_altura(pivot)
        return pivot

    def rotar_izquierda(self, padre):
        pivot = padre.derecha         # pivot SUBE
        padre.derecha = pivot.izquierda
        pivot.izquierda = padre       # padre BAJA
        self.actualizar_altura(padre)
        self.actualizar_altura(pivot)
        return pivot

    # INSERTAR (override)
    def insertar_recursivo(self, nodo_actual, valor):
        # 1. Inserción ABB normal
        if nodo_actual is None:
            return nodo(valor)
        if valor < nodo_actual.valor:
            nodo_actual.izquierda = self.insertar_recursivo(nodo_actual.izquierda, valor)
        elif valor > nodo_actual.valor:
            nodo_actual.derecha = self.insertar_recursivo(nodo_actual.derecha, valor)
        else:
            return nodo_actual  # Sin duplicados

        # 2. Actualizar altura y calcular balance
        self.actualizar_altura(nodo_actual)
        balance = self.get_balance(nodo_actual)

        # 3. Rebalancear según el caso
        if balance > 1 and valor < nodo_actual.izquierda.valor:   # Izq-Izq
            return self.rotar_derecha(nodo_actual)
        if balance < -1 and valor > nodo_actual.derecha.valor:    # Der-Der
            return self.rotar_izquierda(nodo_actual)
        if balance > 1 and valor > nodo_actual.izquierda.valor:   # Izq-Der
            nodo_actual.izquierda = self.rotar_izquierda(nodo_actual.izquierda)
            return self.rotar_derecha(nodo_actual)
        if balance < -1 and valor < nodo_actual.derecha.valor:    # Der-Izq
            nodo_actual.derecha = self.rotar_derecha(nodo_actual.derecha)
            return self.rotar_izquierda(nodo_actual)

        return nodo_actual

    # ELIMINAR (override)
    def eliminar_recursivo(self, nodo_actual, valor):
        # 1. Eliminación ABB normal
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

        # 2. Actualizar altura y calcular balance
        self.actualizar_altura(nodo_actual)
        balance = self.get_balance(nodo_actual)

        # 3. Rebalancear
        if balance > 1 and self.get_balance(nodo_actual.izquierda) >= 0:   # Izq-Izq
            return self.rotar_derecha(nodo_actual)
        if balance > 1 and self.get_balance(nodo_actual.izquierda) < 0:    # Izq-Der
            nodo_actual.izquierda = self.rotar_izquierda(nodo_actual.izquierda)
            return self.rotar_derecha(nodo_actual)
        if balance < -1 and self.get_balance(nodo_actual.derecha) <= 0:    # Der-Der
            return self.rotar_izquierda(nodo_actual)
        if balance < -1 and self.get_balance(nodo_actual.derecha) > 0:     # Der-Izq
            nodo_actual.derecha = self.rotar_derecha(nodo_actual.derecha)
            return self.rotar_izquierda(nodo_actual)

        return nodo_actual
```