from nodo import nodo
from graphviz_class import graphviz_class
import csv


class arbolB:
    def __init__(self, grado):
        # grado/orden m del árbol B (m >= 3)
        # determina cuántas claves e hijos puede tener cada nodo
        self.grado = grado                          # orden m (m >= 3)
        self.claves_min = ((1 + grado) // 2) - 1   # mínimo de claves por nodo (excepto raíz): ceil(m/2) - 1
        self.claves_max = grado - 1                 # máximo de claves por nodo: m - 1
        self.hijos_min = self.claves_min + 1        # mínimo de hijos por nodo interno
        self.hijos_max = grado                      # máximo de hijos por nodo interno (= orden m)
        self.raiz = nodo(es_hoja=True)              # árbol vacío: una sola hoja sin claves
        self.grafica = graphviz_class()             # objeto para generar la representación gráfica

    # ── Búsqueda ────────────────────────────────────────────────────────────

    def buscar(self, clave, nodo_actual=None):
        # busca una clave en el árbol de forma recursiva
        # comienza en la raíz si no se especifica un nodo de inicio
        if nodo_actual is None:
            nodo_actual = self.raiz

        # avanzar por las claves del nodo hasta encontrar una >= clave buscada
        i = 0
        while i < len(nodo_actual.claves) and clave > nodo_actual.claves[i]:
            i += 1

        # si la clave en la posición i coincide, se encontró
        if i < len(nodo_actual.claves) and clave == nodo_actual.claves[i]:
            return True

        # si llegamos a una hoja sin encontrarla, no existe en el árbol
        if nodo_actual.es_hoja:
            return False

        # descender al hijo que corresponde al rango donde debería estar la clave
        return self.buscar(clave, nodo_actual.hijos[i])

    # ── Inserción ────────────────────────────────────────────────────────────

    def insertar(self, clave, actualizar=True):
        # punto de entrada público para insertar una clave en el árbol
        # rechaza duplicados para mantener la propiedad de claves únicas
        if self.buscar(clave):
            print(f"La clave {clave} ya existe en el árbol (duplicado ignorado).")
            return

        # inserción reactiva (bottom-up): se baja hasta la hoja, se inserta,
        # y los splits se propagan hacia arriba sólo si hay overflow
        resultado = self._insertar_recursivo(self.raiz, clave)

        if resultado is not None:
            # la raíz tuvo overflow y fue dividida: se crea una nueva raíz
            # que contiene la clave mediana y apunta a los dos subárboles
            clave_mediana, hijo_derecho = resultado
            nueva_raiz = nodo(es_hoja=False)
            nueva_raiz.claves = [clave_mediana]
            nueva_raiz.hijos = [self.raiz, hijo_derecho]
            self.raiz = nueva_raiz

        # regenerar la imagen del árbol tras la inserción (si se solicita)
        if actualizar:
            self.actualizar_grafica()

    def _insertar_recursivo(self, nodo_actual, clave):
        # función auxiliar recursiva de inserción
        # retorna (clave_mediana, hijo_derecho) si el nodo tiene overflow tras insertar,
        # o None si el nodo quedó dentro de los límites permitidos
        if nodo_actual.es_hoja:
            # caso base: insertar la clave en la posición correcta dentro de la hoja
            # manteniendo el orden ascendente de las claves
            i = 0
            while i < len(nodo_actual.claves) and clave > nodo_actual.claves[i]:
                i += 1
            nodo_actual.claves.insert(i, clave)
        else:
            # nodo interno: determinar en qué hijo descender
            # el hijo i cubre el rango (claves[i-1], claves[i])
            i = 0
            while i < len(nodo_actual.claves) and clave > nodo_actual.claves[i]:
                i += 1
            resultado = self._insertar_recursivo(nodo_actual.hijos[i], clave)

            if resultado is not None:
                # el hijo tuvo overflow y fue dividido
                # absorber la clave mediana que sube e insertar el nuevo hijo derecho
                clave_mediana, hijo_derecho = resultado
                nodo_actual.claves.insert(i, clave_mediana)
                nodo_actual.hijos.insert(i + 1, hijo_derecho)

        # si después de la inserción este nodo supera claves_max, hay overflow
        # se divide y se devuelve la mediana para que el padre la absorba
        if len(nodo_actual.claves) > self.claves_max:
            return self._dividir(nodo_actual)
        return None

    def _dividir(self, nodo_actual):
        # divide un nodo con overflow en dos nodos más pequeños
        # la clave mediana sube al padre para separar ambos subárboles
        #
        # el índice de la mediana depende de la paridad del grado:
        #   grado par   → mediana izquierda: la clave sube al padre primero,
        #                 luego el nuevo hijo derecho recibe las claves restantes
        #   grado impar → mediana central: el nodo nuevo se completa primero,
        #                 luego la clave del centro sube al padre
        n = len(nodo_actual.claves)
        if self.grado % 2 == 0:   # par: mediana izquierda
            medio = (n - 1) // 2
        else:                      # impar: mediana central
            medio = n // 2

        clave_mediana = nodo_actual.claves[medio]

        # crear el nuevo hijo derecho con las claves a la derecha de la mediana
        hijo_derecho = nodo(es_hoja=nodo_actual.es_hoja)
        hijo_derecho.claves = nodo_actual.claves[medio + 1:]
        # el nodo actual conserva sólo las claves a la izquierda de la mediana
        nodo_actual.claves = nodo_actual.claves[:medio]

        # si no es hoja, repartir también los punteros a hijos
        if not nodo_actual.es_hoja:
            hijo_derecho.hijos = nodo_actual.hijos[medio + 1:]
            nodo_actual.hijos = nodo_actual.hijos[:medio + 1]

        return clave_mediana, hijo_derecho

    # ── Eliminación ──────────────────────────────────────────────────────────

    def eliminar(self, clave):
        # punto de entrada público para eliminar una clave del árbol
        # verifica que la clave exista antes de intentar eliminarla
        if not self.buscar(clave):
            print(f"La clave {clave} no existe en el árbol.")
            return

        self._eliminar(self.raiz, clave)

        # si tras la eliminación la raíz quedó sin claves (por una fusión),
        # su único hijo pasa a ser la nueva raíz, reduciendo la altura del árbol
        if len(self.raiz.claves) == 0 and not self.raiz.es_hoja:
            self.raiz = self.raiz.hijos[0]

        # regenerar la imagen del árbol tras la eliminación
        self.actualizar_grafica()

    def _eliminar(self, nodo_actual, clave):
        # función auxiliar recursiva que elimina la clave del subárbol de nodo_actual
        # maneja 3 casos según dónde se encuentre la clave
        min_claves = self.claves_min

        # localizar la posición de la clave dentro del nodo actual
        i = 0
        while i < len(nodo_actual.claves) and clave > nodo_actual.claves[i]:
            i += 1

        if i < len(nodo_actual.claves) and nodo_actual.claves[i] == clave:
            # la clave se encontró en este nodo
            if nodo_actual.es_hoja:
                # caso 1: la clave está en una hoja → se elimina directamente
                # no hay hijos que reorganizar
                nodo_actual.claves.pop(i)
            else:
                # caso 2: la clave está en un nodo interno
                # no se puede eliminar directamente porque tiene hijos
                if len(nodo_actual.hijos[i].claves) > min_claves:
                    # caso 2a: el hijo izquierdo tiene claves de sobra
                    # se reemplaza la clave a eliminar por su predecesor inorden
                    # (el mayor valor del subárbol izquierdo) y se elimina ese predecesor
                    pred = self._get_predecesor(nodo_actual, i)
                    nodo_actual.claves[i] = pred
                    self._eliminar(nodo_actual.hijos[i], pred)
                elif len(nodo_actual.hijos[i + 1].claves) > min_claves:
                    # caso 2b: el hijo derecho tiene claves de sobra
                    # se reemplaza la clave a eliminar por su sucesor inorden
                    # (el menor valor del subárbol derecho) y se elimina ese sucesor
                    succ = self._get_sucesor(nodo_actual, i)
                    nodo_actual.claves[i] = succ
                    self._eliminar(nodo_actual.hijos[i + 1], succ)
                else:
                    # caso 2c: ambos hijos tienen exactamente claves_min claves
                    # se fusionan el hijo izquierdo, la clave a eliminar y el hijo derecho
                    # en un solo nodo, y luego se elimina la clave del nodo fusionado
                    self._merge(nodo_actual, i)
                    self._eliminar(nodo_actual.hijos[i], clave)
        else:
            # la clave no está en este nodo → hay que descender al hijo correcto
            if nodo_actual.es_hoja:
                return  # no debería ocurrir si buscar() validó la existencia

            # antes de descender, garantizar que el hijo destino tenga más de
            # claves_min claves; si no, se le presta una clave o se fusiona
            if len(nodo_actual.hijos[i].claves) <= min_claves:
                i = self._fill(nodo_actual, i)

            self._eliminar(nodo_actual.hijos[i], clave)

    def _get_predecesor(self, nodo_actual, i):
        # obtiene el predecesor inorden de la clave en posición i
        # es el mayor valor del subárbol hijo izquierdo (hijos[i])
        # se llega a él bajando siempre por el hijo más a la derecha
        actual = nodo_actual.hijos[i]
        while not actual.es_hoja:
            actual = actual.hijos[-1]
        return actual.claves[-1]

    def _get_sucesor(self, nodo_actual, i):
        # obtiene el sucesor inorden de la clave en posición i
        # es el menor valor del subárbol hijo derecho (hijos[i+1])
        # se llega a él bajando siempre por el hijo más a la izquierda
        actual = nodo_actual.hijos[i + 1]
        while not actual.es_hoja:
            actual = actual.hijos[0]
        return actual.claves[0]

    def _fill(self, padre, i):
        # garantiza que padre.hijos[i] tenga más de claves_min claves
        # antes de descender a él para eliminar, evitando underflow
        # devuelve el índice del hijo al que se debe descender después
        min_claves = self.claves_min

        if i > 0 and len(padre.hijos[i - 1].claves) > min_claves:
            # el hermano izquierdo tiene claves de sobra: rotar una clave
            # el padre le presta su clave separadora al hijo, y el hermano
            # le presta su clave mayor al padre (rotación hacia la derecha)
            self._borrow_from_prev(padre, i)
            return i
        elif i < len(padre.hijos) - 1 and len(padre.hijos[i + 1].claves) > min_claves:
            # el hermano derecho tiene claves de sobra: rotar una clave
            # el padre le presta su clave separadora al hijo, y el hermano
            # le presta su clave menor al padre (rotación hacia la izquierda)
            self._borrow_from_next(padre, i)
            return i
        else:
            # ningún hermano tiene claves de sobra: fusionar el hijo con un hermano
            # la clave separadora del padre baja al nodo fusionado
            if i < len(padre.hijos) - 1:
                self._merge(padre, i)       # fusionar hijo i con hermano derecho
                return i
            else:
                self._merge(padre, i - 1)   # fusionar hermano izquierdo con hijo i
                return i - 1

    def _borrow_from_prev(self, padre, i):
        # presta una clave del hermano izquierdo (hijos[i-1]) al hijo hijos[i]
        # la clave separadora del padre baja al inicio del hijo,
        # y la clave mayor del hermano sube al padre como nueva separadora
        hijo = padre.hijos[i]
        hermano = padre.hijos[i - 1]

        hijo.claves.insert(0, padre.claves[i - 1])  # la clave del padre baja al hijo
        padre.claves[i - 1] = hermano.claves.pop()  # la última clave del hermano sube al padre

        # si no son hojas, el último hijo del hermano pasa a ser el primer hijo del hijo
        if not hermano.es_hoja:
            hijo.hijos.insert(0, hermano.hijos.pop())

    def _borrow_from_next(self, padre, i):
        # presta una clave del hermano derecho (hijos[i+1]) al hijo hijos[i]
        # la clave separadora del padre baja al final del hijo,
        # y la clave menor del hermano sube al padre como nueva separadora
        hijo = padre.hijos[i]
        hermano = padre.hijos[i + 1]

        hijo.claves.append(padre.claves[i])         # la clave del padre baja al hijo
        padre.claves[i] = hermano.claves.pop(0)     # la primera clave del hermano sube al padre

        # si no son hojas, el primer hijo del hermano pasa a ser el último hijo del hijo
        if not hermano.es_hoja:
            hijo.hijos.append(hermano.hijos.pop(0))

    def _merge(self, padre, i):
        # fusiona hijos[i] con hijos[i+1] usando la clave separadora padre.claves[i]
        # resultado: un solo nodo con claves_min + 1 + claves_min claves
        # el nodo hermano derecho desaparece y el padre pierde una clave
        hijo = padre.hijos[i]
        hermano = padre.hijos[i + 1]

        # la clave separadora del padre baja al centro del nodo fusionado
        hijo.claves.append(padre.claves.pop(i))
        # las claves del hermano derecho se agregan al final
        hijo.claves.extend(hermano.claves)
        # si tienen hijos, los del hermano pasan al hijo izquierdo
        hijo.hijos.extend(hermano.hijos)

        # el hermano derecho ya fue absorbido: se elimina del padre
        padre.hijos.pop(i + 1)

    # ── Carga desde CSV ──────────────────────────────────────────────────────

    def cargar_desde_csv(self, nombre_archivo):
        # lee un archivo CSV con claves enteras separadas por comas
        # e inserta cada valor en el árbol
        # la gráfica se actualiza una sola vez al finalizar la carga
        # para evitar regenerar la imagen en cada inserción individual
        try:
            with open(nombre_archivo, 'r') as archivo:
                lector_csv = csv.reader(archivo)
                count = 0
                for fila in lector_csv:
                    for valor in fila:
                        valor = valor.strip()
                        if valor:
                            self.insertar(int(valor), actualizar=False)
                            count += 1
            self.actualizar_grafica()  # una sola actualización al terminar
            print(f"Se cargaron {count} claves desde '{nombre_archivo}'.")
        except FileNotFoundError:
            print(f"Archivo '{nombre_archivo}' no encontrado.")
        except ValueError as e:
            print(f"Error al leer el archivo: {e}")

    # ── Visualización gráfica ────────────────────────────────────────────────

    def actualizar_grafica(self):
        # regenera la representación visual del árbol desde cero
        # limpia la gráfica anterior, recorre el árbol y guarda la imagen
        self.grafica.limpiar()
        if self.raiz is not None and len(self.raiz.claves) > 0:
            self._recorrer_arbol(self.raiz, None, None)
        self.grafica.guardar(abrir=False)

    def _recorrer_arbol(self, nodo_actual, padre_id, hijo_idx):
        # recorre el árbol en preorden (primero el nodo, luego sus hijos)
        # registra cada nodo y la conexión con su padre en la gráfica
        # usa el id() del objeto Python como identificador único del nodo en el grafo
        node_id = str(id(nodo_actual))
        self.grafica.adicion_nodo(node_id, nodo_actual.claves)

        # si tiene padre, dibujar la arista desde el puerto del padre hasta este nodo
        if padre_id is not None:
            self.grafica.adicion_conexion(padre_id, node_id, hijo_idx)

        # procesar recursivamente cada hijo, pasando el id de este nodo como padre
        if not nodo_actual.es_hoja:
            for i, hijo in enumerate(nodo_actual.hijos):
                self._recorrer_arbol(hijo, node_id, i)
