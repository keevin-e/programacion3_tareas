from nodo import nodo
from graphviz_class import graphviz_class
import csv

class arbolBinario:
    def __init__(self):
        self.raiz = None
        self.grafica = graphviz_class()
    
    #actualiza la grafica del arbol cada vez que se inserta o elimina un nodo
    def actualizar_grafica(self):
        self.grafica.limpiar()
        if self.raiz is not None:
            self.grafica.adicion_nodo(self.raiz.valor)
        self.recorrer_arbol(self.raiz)
        self.grafica.guardar(abrir=False)
        
    #recorre el arbol para agregar los nodos y conexiones a la grafica
    def recorrer_arbol(self, nodo_actual):
        if nodo_actual is not None:
            if nodo_actual.izquierda is not None:
                self.grafica.adicion_nodo(nodo_actual.izquierda.valor,nodo_actual.valor,'izquierda')
                self.recorrer_arbol(nodo_actual.izquierda)
            if nodo_actual.derecha is not None:
                self.grafica.adicion_nodo(nodo_actual.derecha.valor,nodo_actual.valor,'derecha')
                self.recorrer_arbol(nodo_actual.derecha)
     
    #inserta un nuevo nodo en el arbol y actualiza la grafica    
    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = nodo(valor)
        else:
            self.insertar_recursivo(self.raiz, valor)
        self.actualizar_grafica()

    #funcion auxiliar para insertar un nuevo nodo en el arbol de forma recursiva
    def insertar_recursivo(self, nodo_actual, valor):
        if valor < nodo_actual.valor:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = nodo(valor)
            else:
                self.insertar_recursivo(nodo_actual.izquierda, valor)
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = nodo(valor)
            else:
                self.insertar_recursivo(nodo_actual.derecha, valor)
    
    #funcion principal para buscar un valor en el arbol, llama a la funcion auxiliar de forma recursiva
    def buscar(self, valor):
        return self.buscar_recursivo(self.raiz, valor)
    
    #funcion auxiliar para buscar un valor en el arbol de forma recursiva
    def buscar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return False
        if nodo_actual.valor == valor: 
            return True
        elif valor < nodo_actual.valor:
            return self.buscar_recursivo(nodo_actual.izquierda, valor)
        else:
            return self.buscar_recursivo(nodo_actual.derecha, valor) 

    #funcion principal para eliminar un nodo del arbol, llama a la funcion auxiliar de forma recursiva
    def eliminar(self, valor):
        self.raiz = self.eliminar_recursivo(self.raiz, valor)
        self.actualizar_grafica()

    #funcion auxiliar para eliminar un nodo del arbol de forma recursiva
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
            temp = self.encontrar_minimo(nodo_actual.derecha)
            nodo_actual.valor = temp.valor
            nodo_actual.derecha = self.eliminar_recursivo(nodo_actual.derecha, temp.valor)
        return nodo_actual
    
    #funcion para Carga de archivo .csv donde crea un arbol binario con los valores del archivo y actualiza la grafica
    def cargar_desde_csv(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            lector_csv = csv.reader(archivo)
            for fila in lector_csv:
                for valor in fila:
                    self.insertar(int(valor))
    
        

    

