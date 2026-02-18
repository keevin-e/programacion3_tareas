# Programación 3 - Tareas

## Requisito unico (por buenas practicas)
Antes de ejecutar cualquier tarea,  se debe crear y activar un entorno virtual (`venv`) en la raíz del repositorio. para que no de problemas y no instale paquetes con el python global

### 1) Crear el entorno virtual
Desde la raíz del proyecto:

```bash
python3 -m venv .venv
```

### 2) Activar el entorno virtual

```bash
source .venv/bin/activate
```

### 3) Instalar dependencias
Si existe `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Ejecutar tareas
Con el `venv` activo, entra a la subcarpeta de la tarea y ejecuta su script principal.

Ejemplo:

```bash
cd Tarea1
python main.py
```
