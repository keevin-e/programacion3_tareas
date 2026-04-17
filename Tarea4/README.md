# Integrantes para esta tarea
Kevin Eduardo Ruiz Alvarez
9490-25-10092
participación: 100%

# Tarea 4

Instrucciones específicas para ejecutar esta tarea.

## Requisitos
- Haber creado el entorno virtual global en la raíz del repo (`.venv`). opcional
- Tener el entorno virtual activo.
- Tener instaladas las dependencias de `requirements.txt` (Graphviz para Python).

## Ejecutar
Desde la raíz del repositorio:

```bash
source .venv/bin/activate
cd Tarea3
python main.py
```

## Funcionamiento

- al ejecutar el programa se iniciará un menú con 5 opciones
	- 1) Insertar nodo
	- 2) Buscar nodo
	- 3) Eliminar nodo
	- 4) Cargar desde archivo .csv
	- 5) Salir
- Ingresar el número de opción deseada.
- Escribir el dato solicitado por el programa.
- Si se inserta o elimina un nodo, el árbol se actualiza y se genera la gráfica.

## Carga desde CSV

- La opción 4 permite cargar valores enteros desde un archivo `.csv`.
- El archivo debe contener números enteros separados por comas.
- dentro del menu debe escribir el nombre del archivo con su extension .csv
- Ejemplo de contenido válido:

```csv
10,5,20,3,7,15,25
```

## Salida gráfica

- La representación del árbol se guarda en el archivo `grafica.gv`.
- También se genera la imagen del árbol en formato `.png`.
