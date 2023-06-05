# Proyecto Final: 
## Análisis de Rendimiento de Dotplot 
## Secuencial vs Paralelización

El objetivo de este proyecto es implementar y analizar el rendimiento de tres formas de realizar un dotplot, una técnica comúnmente utilizada en bioinformática para comparar secuencias de ADN o proteínas.

### Prerequisitos
El proyecto fue desarrollado usando Python 3.10.9 y con soporte de computación paralela usando librerias multiprocessing y mpi4py. Requiere parámetros de entrada como la secuencia de referencia y de consulta en formato fna que deben declararse en la línea de comandos de ejecución para calcular el dot-plot.

### Instalacion
```
conda create -n PCD-project python=3.10.9
conda activate PCD-project
```

A continuación, instale los paquetes de Python necesarios
```
conda install numpy matplotlib mpi4py
```

Finalmente, descargue el repositorio
```
git clone https://github.com/cristianHenao00/PCD-project.git
```

### Ejecución
Para obtener ayuda, ejecute el siguiente comando:
```
mpirun -np 1 python proyecto.py -h
```
Use: mpirun -np <threads> python proyecto.py -q file.fna ... [options]
