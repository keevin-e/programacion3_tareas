from arbol_binario import arbolBinario

if __name__ == "__main__":
    arbol = arbolBinario()
    while True:
        print("")
        print("---- Menu ----")
        print("1. Insertar nodo")
        print("2. Buscar nodo")
        print("3. Eliminar nodo")
        print("4. Cargar desde archivo .csv")
        print("5. Salir")
        print("-------------")
        opcion = input("Ingrese una opcion: ")
        
        if opcion == "1":
            valor = int(input("Ingrese el valor del nodo a insertar: "))
            arbol.insertar(valor)
        
        elif opcion == "2":
            valor = int(input("Ingrese el valor del nodo a buscar: "))
            encontrado = arbol.buscar(valor)
            if encontrado:
                print(f"El nodo con valor {valor} fue encontrado en el árbol.")
            else:
                print(f"El nodo con valor {valor} no fue encontrado en el árbol.")
        
        elif opcion == "3":
            valor = int(input("Ingrese el valor del nodo a eliminar: "))
            arbol.eliminar(valor)
        
        elif opcion == "4":
            nombre_archivo = input("Ingrese el nombre del archivo .csv (con extensión): ")
            arbol.cargar_desde_csv(nombre_archivo)
        
        elif opcion == "5":
            break
        
        else:
            print("Opción no válida, por favor intente de nuevo.")