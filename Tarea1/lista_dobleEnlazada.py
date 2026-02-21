from nodo import nodo
from graphviz_class import graphviz_class

class listaDoble:
    def __init__(self):
        self.inicio = None
        self.grafica = graphviz_class()

    #explicacion: se recorre la lista desde el inicio, se adiciona cada nodo a la grafica, si el nodo tiene un siguiente, se adiciona la conexion entre el nodo y su siguiente, se guarda la grafica al final
    def actualizar_grafica(self):
        self.grafica.limpiar()
        temporal = self.inicio
        while temporal is not None:
            if temporal.siguiente is not None:
                self.grafica.adicion_conexion(temporal.carnet, temporal.siguiente.carnet)
                self.grafica.adicion_conexion(temporal.siguiente.carnet, temporal.carnet)
            temporal = temporal.siguiente
        self.grafica.guardar(abrir=False)

    def insertar_al_principio(self, carnet, nombre, apellido):
        self.nuevo_nodo = nodo(carnet, nombre, apellido)
        if self.inicio is None:
            self.inicio = self.nuevo_nodo
            
        else:
            ##Recordatorio: el nuevo nodo apunta al inicio, el inicio apunta al nuevo nodo y el nuevo nodo se convierte en el inicio
            self.nuevo_nodo.siguiente = self.inicio
            self.inicio.anterior = self.nuevo_nodo
            self.inicio = self.nuevo_nodo
        self.actualizar_grafica()
    
    def insertar_al_final(self, carnet, nombre, apellido):
        self.nuevo_nodo = nodo(carnet, nombre, apellido)
        if self.inicio is None:
            self.inicio = self.nuevo_nodo
        else:
            ##Recordatorio: se recorre la lista hasta el final, el último nodo apunta al nuevo nodo y el nuevo nodo apunta al último nodo
            self.temporal = self.inicio
            while self.temporal.siguiente is not None:
                self.temporal = self.temporal.siguiente
            self.temporal.siguiente = self.nuevo_nodo
            self.nuevo_nodo.anterior = self.temporal
        self.actualizar_grafica()

    def eliminar_por_carnet(self, carnet):
        if self.inicio is None:
            print("La lista está vacía")
        else:
            self.temporal = self.inicio
            while self.temporal is not None:
                if self.temporal.carnet == carnet:
                    #Recordatorio: si el nodo a eliminar no es el inicio, el nodo.anterior apunta al nodo siguiente, si el nodo a eliminar es el inicio, el inicio apunta al nodo siguiente, si el nodo a eliminar no es el final, el nodo siguiente apunta al nodo anterior
                    if self.temporal.anterior is not None:
                        self.temporal.anterior.siguiente = self.temporal.siguiente
                    else:
                        self.inicio = self.temporal.siguiente
                    if self.temporal.siguiente is not None:
                        self.temporal.siguiente.anterior = self.temporal.anterior
                    self.actualizar_grafica()
                    return
                self.temporal = self.temporal.siguiente
            print("No se encontró el carnet en la lista")
            
    def mostrar_lista(self):
        if self.inicio is None:
            print("None -> None")
        else:
            self.temporal = self.inicio
            lista = "None <- "
            while self.temporal is not None:
                lista += f"{self.temporal.carnet} "
                if self.temporal.siguiente is not None:
                    lista += " <-> "
                self.temporal = self.temporal.siguiente
            lista += "-> None"
            print(lista)
        
        