import csv


# Centinela para distinguir "no encontrado" de "encontrado con datos=None"
class _NotFound:
    def __repr__(self):
        return "NOT_FOUND"
    def __bool__(self):
        return False

NOT_FOUND = _NotFound()


def leer_csv(archivo, columna_clave, convertir_numero=True):
    """
    Lee un CSV y retorna (registros, errores).
    registros: lista de (clave, dict_fila)
    errores:   cantidad de filas omitidas por clave vacía o nula
    """
    registros = []
    errores = 0
    with open(archivo, 'r', encoding='utf-8', errors='replace') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            clave = fila.get(columna_clave)
            if clave is None:
                errores += 1
                continue
            clave = clave.strip()
            if not clave:
                errores += 1
                continue
            if convertir_numero:
                try:
                    clave = float(clave)
                except (ValueError, TypeError):
                    pass
            registros.append((clave, dict(fila)))
    return registros, errores


def comparar_claves(a, b):
    """
    Compara dos claves retornando -1, 0 o 1.
    Maneja comparaciones entre tipos incompatibles (str vs float)
    convirtiendo ambos a str como fallback.
    """
    try:
        if a < b:
            return -1
        if a > b:
            return 1
        return 0
    except TypeError:
        a, b = str(a), str(b)
        if a < b:
            return -1
        if a > b:
            return 1
        return 0
