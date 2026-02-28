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

def convertir_a_decimal(numero_romano, index):
    valores = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }

    if index >= len(numero_romano):
        return 0

    valor_actual = valores.get(numero_romano[index].upper(), 0)

    if index + 1 < len(numero_romano):
        valor_siguiente = valores.get(numero_romano[index + 1].upper(), 0)
        if valor_actual < valor_siguiente:
            return valor_siguiente - valor_actual + convertir_a_decimal(numero_romano, index + 2)

    return valor_actual + convertir_a_decimal(numero_romano, index + 1)

#funcion para calcular la raiz cuadrada entera de un numero entero positivo con una función recursiva auxiliar
def raiz_cuadrada_entera(numero):
    if numero < 0:
        return "No se puede calcular la raíz cuadrada de un número negativo"
    return calcular_raiz_cuadrada(numero)

def calcular_raiz_cuadrada(numero, raiz=0):
    if (raiz + 1) * (raiz + 1) > numero:
        return raiz
    return calcular_raiz_cuadrada(numero, raiz + 1)


