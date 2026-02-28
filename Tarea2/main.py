from funciones import convertir_a_binario, contar_digitos, suma_numeros_enteros, raiz_cuadrada_entera,convertir_a_decimal


if __name__ == "__main__":
    while True:
        print("")
        print("---- Menu ----")
        print("1. Convertir a binario")
        print("2. Contar dígitos")
        print("3. Raíz cuadrada entera")
        print("4. Convertir a Decimal desde Romano")
        print("5. Suma de Numeros Enteros")
        print("6. Salir")
        print("-------------")
        opcion = input("Ingrese una opcion: ")
        
        if opcion == "1":
            numero = int(input("Ingrese un numero: "))
            resultado = convertir_a_binario(numero)
            print(f"El numero {numero} en binario es: {resultado}")
        
        elif opcion == "2":
            numero = int(input("Ingrese un numero: "))
            resultado = contar_digitos(numero)
            print(f"El numero {numero} tiene {resultado} digitos.")
        
        elif opcion == "3":
            numero = int(input("Ingrese un numero: "))
            resultado = raiz_cuadrada_entera(numero)
            print(f"La raíz cuadrada entera de {numero} es: {resultado}")
            
        elif opcion == "4":
            numero_romano = input("Ingrese un numero romano: ")
            resultado = convertir_a_decimal(numero_romano, 0)
            print(f"El numero romano {numero_romano} en decimal es: {resultado}")
        
        elif opcion == "5":
            numero = int(input("Ingrese un numero: "))
            resultado = suma_numeros_enteros(numero)
            print(f"La suma de los numeros enteros desde 0 hasta {numero} es: {resultado}")    
        
        elif opcion == "6":
            break
        
        else:
            print("opcion no valida")