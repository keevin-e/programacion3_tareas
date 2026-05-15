from arbol_b import arbolB

if __name__ == "__main__":
    print("---- Árbol B ----")
    while True:
        try:
            grado = int(input("Ingrese el grado del Árbol B (m >= 3): "))
            if grado >= 3:
                break
            print("El grado mínimo debe ser mayor o igual a 3.")
        except ValueError:
            print("Ingrese un número entero válido.")

    arbol = arbolB(grado)
    claves_min = ((1 + grado) // 2) - 1
    claves_max = grado - 1
    print(f"Árbol B creado con grado m = {grado}")
    print(f"Cada nodo tendrá {claves_min} claves minimas  y {claves_max} claves maximas.")

    while True:
        print("")
        print("---- Menu ----")
        print("1. Insertar clave")
        print("2. Buscar clave")
        print("3. Eliminar clave")
        print("4. Cargar desde archivo .csv")
        print("5. Salir")
        print("-------------")
        opcion = input("Ingrese una opcion: ")

        if opcion == "1":
            try:
                clave = int(input("Ingrese la clave a insertar: "))
                arbol.insertar(clave)
                print(f"Clave {clave} insertada.")
            except ValueError:
                print("Ingrese un número entero válido.")

        elif opcion == "2":
            try:
                clave = int(input("Ingrese la clave a buscar: "))
                encontrado = arbol.buscar(clave)
                if encontrado:
                    print(f"La clave {clave} fue encontrada en el árbol.")
                else:
                    print(f"La clave {clave} no fue encontrada en el árbol.")
            except ValueError:
                print("Ingrese un número entero válido.")

        elif opcion == "3":
            try:
                clave = int(input("Ingrese la clave a eliminar: "))
                arbol.eliminar(clave)
            except ValueError:
                print("Ingrese un número entero válido.")

        elif opcion == "4":
            nombre_archivo = input("Ingrese el nombre del archivo .csv (con extensión): ")
            arbol.cargar_desde_csv(nombre_archivo)

        elif opcion == "5":
            break

        else:
            print("Opción no válida, por favor intente de nuevo.")
