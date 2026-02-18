from nodo import nodo

class listaDoble:
    def __init__(self):
        self.inicio = None

    def insertar_al_principio(self, carnet, nombre, apellido):
        self.nuevo_nodo = nodo(carnet, nombre, apellido)
        if self.inicio is None:
            self.inicio = self.nuevo_nodo
        else:
            ##retroalimentacion para mi (y que no me confunda): el nuevo nodo apunta al inicio, el inicio apunta al nuevo nodo y el nuevo nodo se convierte en el inicio
            self.nuevo_nodo.siguiente = self.inicio
            self.inicio.anterior = self.nuevo_nodo
            self.inicio = self.nuevo_nodo
    
    def insertar_al_final(self, carnet, nombre, apellido):
        self.nuevo_nodo = nodo(carnet, nombre, apellido)
        if self.inicio is None:
            self.inicio = self.temporal
        else:
            ##retroalimentacion para mi (y que no me confunda): se recorre la lista hasta el final, el último nodo apunta al nuevo nodo y el nuevo nodo apunta al último nodo
            self.temporal = self.inicio
            while self.temporal.siguiente is not None:
                self.temporal = self.temporal.siguiente
            self.temporal.siguiente = self.nuevo_nodo
            self.nuevo_nodo.anterior = self.temporal

    def eliminar_por_carnet(self, carnet):
        if self.inicio is None:
            print("La lista está vacía")
        else:
            self.temporal = self.inicio
            while self.temporal is not None:
                if self.temporal.carnet == carnet:
                    #retroalimentacion para mi (y que no me confunda): si el nodo a eliminar no es el inicio, el nodo anterior apunta al nodo siguiente, si el nodo a eliminar es el inicio, el inicio apunta al nodo siguiente, si el nodo a eliminar no es el final, el nodo siguiente apunta al nodo anterior
                    if self.temporal.anterior is not None:
                        self.temporal.anterior.siguiente = self.temporal.siguiente
                    else:
                        self.inicio = self.temporal.siguiente
                    if self.temporal.siguiente is not None:
                        self.temporal.siguiente.anterior = self.temporal.anterior
                    return
                self.temporal = self.temporal.siguiente
            print("No se encontró el carnet en la lista")
            
    #def mostrar_lista(self):
    #    self.temporal = self.inicio
        