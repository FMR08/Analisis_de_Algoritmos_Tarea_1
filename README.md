# Guía de Ejecución

## 1. Librerías Necesarias a Instalar

Para instalar las dependencias requeridas para la recolección de datos y generación de gráficos, ejecuta el siguiente comando en tu terminal:

```bash
pip install pandas matplotlib
```
## 2. Comandos para Ejecutar el Código

Para asegurar el correcto funcionamiento del programa, 
es indispensable situar la terminal en el directorio 
raíz donde se encuentran almacenados los módulos fuente 
(`.py`). Asimismo, el proceso consta de dos fases secuenciales 
que deben respetarse de manera estricta: 
1. en primer lugar, se debe ejecutar `main.py` para llevar a cabo 
la recolección de métricas empíricas y la exportación de los archivos 
estructurados `.csv`. 
2. En segundo lugar, se invocará `plot.py` 
para procesar dicha información y generar las representaciones gráficas
correspondientes.

### En Windows (Usando CMD o PowerShell)
1. python main.py 
2. python plot.py

### En Linux / macOS
1. python3 main.py 
2. python3 plot.py