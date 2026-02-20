from nodo import nodo
from lista_dobleEnlazada import listaDoble
from graphviz_class import graphviz_class


if __name__ == "__main__":
    lista = listaDoble()
    while True:
        print("")
        print("---- Menu ----")
        print("1. Insertar al principio")
        print("2. Insertar al final")
        print("3. Eliminar por carnet")
        print("4. Mostrar lista")
        print("5. Salir")
        print("-------------")
        opcion = input("Ingrese una opción: ")
        if opcion == "1":
            carnet = input("Ingrese el carnet: ")
            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            lista.insertar_al_principio(carnet, nombre, apellido)
        elif opcion == "2":
            carnet = input("Ingrese el carnet: ")
            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            lista.insertar_al_final(carnet, nombre, apellido)
        elif opcion == "3":
            carnet = input("Ingrese el carnet a eliminar: ")
            lista.eliminar_por_carnet(carnet)
        elif opcion == "4":
            lista.mostrar_lista()
        elif opcion == "5":
            break
        else:
            print("Opción no válida")
            