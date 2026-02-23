
# Función para convertir un número entero positivo a su binario
def convertir_a_binario(numero_entero):
    if numero_entero <= 0:
        return "0"
    elif numero_entero == 1:
        return "1"
    else:
        return convertir_a_binario(numero_entero // 2) + str(numero_entero % 2)

#funcion para contar los digitos de un numero entero positivo
def contar_digitos(numero_entero):
    entero_str = str(numero_entero)
    if len(entero_str) <= 0:
        return 0
    return 1 + contar_digitos(entero_str[:-1])

# Función para sumar los números enteros desde cero hasta un número entero positivo dado
def suma_numeros_enteros(numero_entero):
    if numero_entero <= 0:
        return 0
    if numero_entero == 1:
        return 1
    
    resultado = numero_entero + suma_numeros_enteros(numero_entero - 1)
    return resultado