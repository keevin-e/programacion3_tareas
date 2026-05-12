import time
import random
import os

from utils import leer_csv


class Experimento:
    """
    Mide y compara los tiempos de inserción, búsqueda y eliminación
    sobre las tres estructuras de datos: Lista Simple, ABB y AVL.

    Uso típico:
        exp = Experimento()
        exp.cargar_csv("datos.csv", "id")
        exp.ejecutar_todas()
        exp.mostrar_resultados()
        exp.generar_grafica()
    """

    def __init__(self):
        self.datos = []           # Lista de (clave, dict_fila)
        self.resultados = []      # Lista de dicts con tiempos por estructura

    # ------------------------------------------------------------------
    # Carga de datos
    # ------------------------------------------------------------------

    def cargar_csv(self, archivo, columna_clave, convertir_numero=True):
        """
        Lee el CSV y almacena los registros en memoria para reutilizarlos
        en múltiples estructuras sin releer el archivo.
        Retorna la cantidad de registros cargados.
        """
        self.datos, errores = leer_csv(archivo, columna_clave, convertir_numero)
        self.resultados.clear()
        print(f"  Registros cargados: {len(self.datos)}  |  Omitidos (clave vacía): {errores}")
        return len(self.datos)

    # ------------------------------------------------------------------
    # Ejecución del experimento sobre una estructura
    # ------------------------------------------------------------------

    def ejecutar(self, estructura, nombre, n_busquedas=200, n_eliminaciones=200):
        """
        Carga todos los datos en 'estructura', luego mide:
          - Tiempo total de inserción (todos los registros)
          - Tiempo total de búsqueda  (muestra aleatoria de n_busquedas claves)
          - Tiempo total de eliminación (muestra aleatoria de n_eliminaciones claves)

        Retorna un dict con los tiempos y metadatos.
        """
        if not self.datos:
            print("No hay datos cargados. Use cargar_csv() primero.")
            return None

        n = len(self.datos)
        n_busq = min(n_busquedas, n)
        n_elim = min(n_eliminaciones, n)

        indices = list(range(n))

        # ---------- Inserción ----------
        t0 = time.perf_counter()
        for clave, fila in self.datos:
            estructura.insertar(clave, fila)
        t_insercion = time.perf_counter() - t0

        # ---------- Búsqueda ----------
        muestra_busq = [self.datos[i][0] for i in random.sample(indices, n_busq)]
        t0 = time.perf_counter()
        for clave in muestra_busq:
            estructura.buscar(clave)
        t_busqueda = time.perf_counter() - t0

        # ---------- Eliminación ----------
        muestra_elim = [self.datos[i][0] for i in random.sample(indices, n_elim)]
        t0 = time.perf_counter()
        for clave in muestra_elim:
            estructura.eliminar(clave)
        t_eliminacion = time.perf_counter() - t0

        resultado = {
            'nombre':           nombre,
            'n_datos':          n,
            'n_busquedas':      n_busq,
            'n_eliminaciones':  n_elim,
            't_insercion':      t_insercion,
            't_busqueda':       t_busqueda,
            't_eliminacion':    t_eliminacion,
        }
        self.resultados.append(resultado)
        return resultado

    # ------------------------------------------------------------------
    # Ejecución sobre las 3 estructuras de un solo comando
    # ------------------------------------------------------------------

    def ejecutar_todas(self, n_busquedas=200, n_eliminaciones=200):
        """Crea instancias frescas de las 3 estructuras y ejecuta el experimento."""
        from lista_simple import ListaSimple
        from arbol_binario import ArbolBinario
        from arbol_avl import ArbolAVL

        self.resultados.clear()

        estructuras = [
            (ListaSimple,   "Lista Simple"),
            (ArbolBinario,  "ABB"),
            (ArbolAVL,      "AVL"),
        ]

        for Clase, nombre in estructuras:
            print(f"  [{nombre}]...", end=' ', flush=True)
            instancia = Clase()
            r = self.ejecutar(instancia, nombre, n_busquedas, n_eliminaciones)
            print(f"Inserción: {r['t_insercion']:.4f}s  |  "
                  f"Búsqueda: {r['t_busqueda']:.4f}s  |  "
                  f"Eliminación: {r['t_eliminacion']:.4f}s")

    # ------------------------------------------------------------------
    # Mostrar resultados en tabla
    # ------------------------------------------------------------------

    def mostrar_resultados(self):
        if not self.resultados:
            print("\nNo hay resultados. Ejecute el experimento primero.")
            return

        sep = "=" * 78
        print(f"\n{sep}")
        print("  RESULTADOS DEL EXPERIMENTO")
        print(sep)

        for r in self.resultados:
            n   = r['n_datos']
            nb  = r['n_busquedas']
            ne  = r['n_eliminaciones']
            ti  = r['t_insercion']
            tb  = r['t_busqueda']
            te  = r['t_eliminacion']

            print(f"\n  Estructura : {r['nombre']}")
            print(f"  Registros  : {n}")
            print(f"  {'Operación':<14} {'Total (s)':>12} {'Ops medidas':>12} {'Promedio (µs/op)':>18}")
            print(f"  {'-' * 58}")
            print(f"  {'Inserción':<14} {ti:>12.6f} {n:>12} {(ti / n) * 1e6:>18.3f}")
            print(f"  {'Búsqueda':<14} {tb:>12.6f} {nb:>12} {(tb / nb) * 1e6:>18.3f}")
            print(f"  {'Eliminación':<14} {te:>12.6f} {ne:>12} {(te / ne) * 1e6:>18.3f}")

        print(f"\n{sep}")

        # Tabla comparativa de promedios
        print("\n  COMPARATIVA RÁPIDA — Promedio por operación (µs)")
        print(f"  {'Estructura':<16} {'Inserción':>14} {'Búsqueda':>14} {'Eliminación':>14}")
        print(f"  {'-' * 60}")
        for r in self.resultados:
            n, nb, ne = r['n_datos'], r['n_busquedas'], r['n_eliminaciones']
            print(f"  {r['nombre']:<16} "
                  f"{(r['t_insercion']/n)*1e6:>14.3f} "
                  f"{(r['t_busqueda']/nb)*1e6:>14.3f} "
                  f"{(r['t_eliminacion']/ne)*1e6:>14.3f}")
        print(f"\n{sep}\n")

    # ------------------------------------------------------------------
    # Gráfica comparativa
    # ------------------------------------------------------------------

    def generar_grafica(self):
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib no disponible. Instálelo con: pip install matplotlib")
            return

        if not self.resultados:
            print("No hay resultados. Ejecute el experimento primero.")
            return

        nombres = [r['nombre'] for r in self.resultados]
        n_datos = [r['n_datos'] for r in self.resultados]
        n_busq  = [r['n_busquedas'] for r in self.resultados]
        n_elim  = [r['n_eliminaciones'] for r in self.resultados]

        # Promedios en µs por operación
        ins_avg = [(r['t_insercion'] / n) * 1e6 for r, n in zip(self.resultados, n_datos)]
        bus_avg = [(r['t_busqueda']  / nb) * 1e6 for r, nb in zip(self.resultados, n_busq)]
        eli_avg = [(r['t_eliminacion'] / ne) * 1e6 for r, ne in zip(self.resultados, n_elim)]

        # Totales en segundos
        ins_tot = [r['t_insercion']   for r in self.resultados]
        bus_tot = [r['t_busqueda']    for r in self.resultados]
        eli_tot = [r['t_eliminacion'] for r in self.resultados]

        x = list(range(len(nombres)))
        w = 0.25
        colores = ['steelblue', 'darkorange', 'seagreen']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # --- Gráfica 1: tiempo total ---
        for i, (vals, label, color) in enumerate(zip(
                [ins_tot, bus_tot, eli_tot],
                ['Inserción', 'Búsqueda', 'Eliminación'],
                colores)):
            ax1.bar([xi + (i - 1) * w for xi in x], vals, w, label=label, color=color)
        ax1.set_title('Tiempo total por operación (s)')
        ax1.set_ylabel('Tiempo (s)')
        ax1.set_xlabel('Estructura')
        ax1.set_xticks(x)
        ax1.set_xticklabels(nombres)
        ax1.legend()

        # --- Gráfica 2: promedio por operación ---
        for i, (vals, label, color) in enumerate(zip(
                [ins_avg, bus_avg, eli_avg],
                ['Inserción', 'Búsqueda', 'Eliminación'],
                colores)):
            ax2.bar([xi + (i - 1) * w for xi in x], vals, w, label=label, color=color)
        ax2.set_title('Tiempo promedio por operación (µs)')
        ax2.set_ylabel('Tiempo (µs)')
        ax2.set_xlabel('Estructura')
        ax2.set_xticks(x)
        ax2.set_xticklabels(nombres)
        ax2.legend()

        fig.suptitle(
            f'Comparación de Estructuras de Datos  '
            f'({self.resultados[0]["n_datos"]:,} registros)',
            fontsize=13, fontweight='bold'
        )
        plt.tight_layout()

        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resultados_experimento.png')
        plt.savefig(ruta, dpi=150, bbox_inches='tight')
        print(f"\nGráfica guardada en: {ruta}")

        try:
            plt.show()
        except Exception:
            pass
