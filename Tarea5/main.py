import sys
import os
import csv
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lista_simple import ListaSimple
from arbol_binario import ArbolBinario
from arbol_avl import ArbolAVL
from utils import leer_csv, NOT_FOUND


# ---------------------------------------------------------------------------
# Estado global de la sesión
# ---------------------------------------------------------------------------
datos_cargados = []           # Lista de (clave, dict_fila) leídos del CSV
estructura_actual = None      # Instancia activa de la estructura
nombre_estructura = ""        # Nombre legible de la estructura activa
tiempos = []                  # Historial: [{'operacion', 'clave', 'tiempo_us'}, ...]
convertir_num_activo = False  # Mismo modo de conversión que se usó al cargar el CSV


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def pausar():
    input("\nPresione Enter para continuar...")


def titulo(texto):
    print("\n" + "=" * 52)
    print(f"  {texto}")
    print("=" * 52)


def inspeccionar_csv(archivo):
    """Muestra columnas y primeras filas del CSV para ayudar al usuario."""
    try:
        with open(archivo, 'r', encoding='utf-8', errors='replace') as f:
            lector = csv.DictReader(f)
            columnas = lector.fieldnames or []
            print(f"\n  Columnas encontradas ({len(columnas)}):")
            for i, col in enumerate(columnas, 1):
                print(f"    {i:>3}. {col}")
            print("\n  Primeras 3 filas (primeros 4 campos):")
            for idx, fila in enumerate(lector):
                if idx >= 3:
                    break
                preview = dict(list(fila.items())[:4])
                print(f"    {preview}")
        return columnas
    except FileNotFoundError:
        print(f"\n  Error: no se encontró el archivo → {archivo}")
        return None
    except Exception as e:
        print(f"\n  Error al leer el archivo: {e}")
        return None


def _convertir_clave(texto):
    """Convierte al mismo tipo usado al cargar el CSV."""
    if convertir_num_activo:
        try:
            return float(texto)
        except ValueError:
            pass
    return texto


def fmt_tiempo(s):
    """Devuelve el tiempo formateado en segundos o milisegundos."""
    if s >= 1.0:
        return f"{s:.3f} s"
    return f"{s * 1000:.3f} ms"


def registrar(operacion, clave, duracion_s):
    tiempos.append({
        'operacion': operacion,
        'clave': clave,
        'tiempo_s': duracion_s,
    })


# ---------------------------------------------------------------------------
# Opción 1: Cargar CSV
# ---------------------------------------------------------------------------

def cargar_datos():
    global datos_cargados, convertir_num_activo

    titulo("CARGAR DATOS DESDE CSV")
    archivo = input("  Ruta del archivo CSV: ").strip()
    if not archivo:
        return

    columnas = inspeccionar_csv(archivo)
    if not columnas:
        pausar()
        return

    while True:
        try:
            num = int(input("\n  Seleccione la columna clave (número): ").strip())
            if 1 <= num <= len(columnas):
                columna_clave = columnas[num - 1]
                print(f"  Columna seleccionada: {columna_clave}")
                break
            print(f"  Ingrese un número entre 1 y {len(columnas)}.")
        except ValueError:
            print("  Ingrese un número válido.")

    conv = input("  ¿Convertir clave a número? (s/n, default=s): ").strip().lower()
    convertir = conv != 'n'
    convertir_num_activo = convertir

    datos_cargados, errores = leer_csv(archivo, columna_clave, convertir)
    print(f"\n  Registros cargados : {len(datos_cargados)}")
    if errores:
        print(f"  Omitidos (filas con clave vacía o nula): {errores}")
    pausar()


# ---------------------------------------------------------------------------
# Opción 2: Seleccionar estructura
# ---------------------------------------------------------------------------

def seleccionar_estructura():
    global estructura_actual, nombre_estructura, tiempos

    titulo("SELECCIONAR ESTRUCTURA")
    print("  1. Lista Simple")
    print("  2. Árbol Binario de Búsqueda (ABB)")
    print("  3. Árbol AVL")
    print("  4. Volver")

    op = input("\n  Opción: ").strip()
    mapa = {
        '1': (ListaSimple,  "Lista Simple"),
        '2': (ArbolBinario, "ABB"),
        '3': (ArbolAVL,     "AVL"),
    }
    if op not in mapa:
        return

    Clase, nombre = mapa[op]
    estructura_actual = Clase()
    nombre_estructura = nombre
    tiempos.clear()
    print(f"\n  Estructura activa: {nombre_estructura}")
    print("  (historial de tiempos reiniciado)")
    pausar()


# ---------------------------------------------------------------------------
# Opción 3: Operaciones
# ---------------------------------------------------------------------------

def op_insertar():
    titulo(f"INSERTAR  [{nombre_estructura}]")
    print("  1. Insertar todos los datos del CSV")
    print("  2. Insertar un valor manualmente")
    print("  3. Volver")
    op = input("\n  Opción: ").strip()

    if op == '1':
        if not datos_cargados:
            print("\n  No hay datos cargados. Use la opción 1 del menú principal.")
            pausar()
            return
        n = len(datos_cargados)
        t0 = time.perf_counter()
        for clave, fila in datos_cargados:
            estructura_actual.insertar(clave, fila)
        duracion = time.perf_counter() - t0
        registrar("Inserción (masiva)", f"{n} registros", duracion)
        print(f"\n  {n} registros insertados")
        print(f"  Tiempo total : {fmt_tiempo(duracion)}")
        print(f"  Promedio     : {fmt_tiempo(duracion / n)}/op")

    elif op == '2':
        clave = _convertir_clave(input("  Clave: ").strip())
        t0 = time.perf_counter()
        estructura_actual.insertar(clave)
        duracion = time.perf_counter() - t0
        registrar("Inserción", clave, duracion)
        print(f"  Insertado: {clave}  |  Tiempo: {fmt_tiempo(duracion)}")

    pausar()


def op_buscar():
    titulo(f"BUSCAR  [{nombre_estructura}]")

    if estructura_actual.tamanio == 0:
        print("\n  La estructura está vacía. Use 'Insertar' primero.")
        pausar()
        return

    clave = _convertir_clave(input("  Clave a buscar: ").strip())

    t0 = time.perf_counter()
    resultado = estructura_actual.buscar(clave)
    duracion = time.perf_counter() - t0
    registrar("Búsqueda", clave, duracion)

    if resultado is not NOT_FOUND:
        if isinstance(resultado, dict):
            preview = dict(list(resultado.items())[:6])
            print(f"\n  Encontrado: {preview}")
        elif resultado is None:
            print("\n  Encontrado (sin datos extra).")
        else:
            print(f"\n  Encontrado: {resultado}")
    else:
        print(f"\n  No encontrado. (La estructura tiene {estructura_actual.tamanio} nodos)")
    print(f"  Tiempo: {fmt_tiempo(duracion)}")
    pausar()


def op_eliminar():
    titulo(f"ELIMINAR  [{nombre_estructura}]")
    clave = _convertir_clave(input("  Clave a eliminar: ").strip())

    t0 = time.perf_counter()
    ok = estructura_actual.eliminar(clave)
    duracion = time.perf_counter() - t0
    registrar("Eliminación", clave, duracion)

    print(f"\n  {'Eliminado.' if ok else 'Clave no encontrada.'}")
    print(f"  Tiempo: {fmt_tiempo(duracion)}")
    pausar()


def ver_tiempos():
    titulo(f"TIEMPOS REGISTRADOS  [{nombre_estructura}]")
    if not tiempos:
        print("  Sin registros todavía.")
        pausar()
        return

    print(f"  {'#':<4} {'Operación':<25} {'Clave':<20} {'Tiempo':>12}")
    print("  " + "-" * 63)
    for i, r in enumerate(tiempos, 1):
        clave_str = str(r['clave'])[:18]
        print(f"  {i:<4} {r['operacion']:<25} {clave_str:<20} {fmt_tiempo(r['tiempo_s']):>12}")

    # Resumen agrupado por tipo de operación
    print()
    tipos = {}
    for r in tiempos:
        tipos.setdefault(r['operacion'], []).append(r['tiempo_s'])
    print(f"  {'Operación':<25} {'Ops':>5} {'Promedio':>14} {'Total':>12}")
    print("  " + "-" * 58)
    for op, vals in tipos.items():
        print(f"  {op:<25} {len(vals):>5} {fmt_tiempo(sum(vals)/len(vals)):>14} {fmt_tiempo(sum(vals)):>12}")

    pausar()


def menu_operaciones():
    if estructura_actual is None:
        print("\n  No hay estructura seleccionada. Use la opción 2 del menú principal.")
        pausar()
        return

    while True:
        titulo(f"OPERACIONES  [{nombre_estructura}  |  n={estructura_actual.tamanio}]")
        print("  1. Insertar")
        print("  2. Buscar")
        print("  3. Eliminar")
        print("  4. Ver tiempos registrados")
        print("  5. Volver")

        op = input("\n  Opción: ").strip()
        if op == '1':
            op_insertar()
        elif op == '2':
            op_buscar()
        elif op == '3':
            op_eliminar()
        elif op == '4':
            ver_tiempos()
        elif op == '5':
            break


# ---------------------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------------------

def menu_principal():
    while True:
        titulo("ESTRUCTURAS DE DATOS — COMPARACIÓN")
        print(f"  Datos en memoria : {len(datos_cargados)} registros")
        print(f"  Estructura activa: {nombre_estructura or '(ninguna)'}")
        print("─" * 52)
        print("  1. Cargar datos desde CSV")
        print("  2. Seleccionar estructura")
        print("  3. Operaciones (Insertar / Buscar / Eliminar)")
        print("  4. Salir")
        print("=" * 52)

        opcion = input("  Opción: ").strip()
        if opcion == '1':
            cargar_datos()
        elif opcion == '2':
            seleccionar_estructura()
        elif opcion == '3':
            menu_operaciones()
        elif opcion == '4':
            print("\n  ¡Hasta luego!\n")
            break
        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    menu_principal()
