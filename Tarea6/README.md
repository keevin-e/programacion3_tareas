# Integrantes para esta tarea
Kevin Eduardo Ruiz Alvarez
9490-25-10092
participación: 100%

# Tarea 6 — Árbol B

Implementación de un **Árbol B configurable por grado mínimo** en Python, con las operaciones de inserción, búsqueda y eliminación de claves, carga masiva desde archivos CSV y visualización gráfica mediante Graphviz.

## Requisitos
- Haber creado el entorno virtual global en la raíz del repo (`.venv`). opcional
- Tener el entorno virtual activo.
- Tener instaladas las dependencias de `requirements.txt` (Graphviz para Python).

## Ejecutar
Desde la raíz del repositorio:

```bash
source .venv/bin/activate
cd Tarea6
python main.py
```

## Configuración inicial

Al iniciar el programa se solicita el **grado mínimo `t`** del Árbol B (debe ser `t >= 3`).

## Funcionamiento

Al ejecutar el programa se mostrará un menú con 5 opciones:
- `1` Insertar clave
- `2` Buscar clave
- `3` Eliminar clave
- `4` Cargar desde archivo `.csv`
- `5` Salir

Ingresar el número de opción deseada y escribir el dato solicitado.

Cada inserción o eliminación genera automáticamente la gráfica actualizada del árbol.

## Carga desde CSV

La opción `4` permite cargar claves enteras desde un archivo `.csv`.

### Formato del archivo
El archivo debe contener números enteros separados por comas (sin encabezado):

```csv
15,42,7,98,23,61,...
```

### Cómo cargar los archivos incluidos

Se incluyen dos archivos de prueba en la carpeta `Tarea6/`:

Para cargarlos, seleccionar la opción `4` del menú e ingresar el nombre del archivo:

```
Ingrese el nombre del archivo .csv (con extensión): prueba1.csv
```

> El programa debe ejecutarse **desde la carpeta `Tarea6/`** para que los archivos sean encontrados por nombre relativo. De lo contrario, ingresar la ruta completa, por ejemplo:
> `../Tarea6/prueba1.csv`

## Salida gráfica

- La representación del árbol se guarda en `Tarea6/grafica.gv`.
- También se genera la imagen del árbol en formato `.png` (`grafica.gv.png`).
- Cada nodo del árbol B se muestra como un rectángulo con todas sus claves. Las aristas conectan cada ranura del nodo padre con el nodo hijo correspondiente.
