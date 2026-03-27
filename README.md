# Minesweeper Engine - Proyecto UBA 💣

Este es un proyecto grupal desarrollado para la carrera de **Ciencia de Datos en la Universidad de Buenos Aires (UBA)**. El objetivo fue crear la lógica funcional de un Buscaminas desde cero en Python.

## Mi participación en el proyecto
Aunque fue un trabajo colaborativo en el que participé en el desarrollo general, mi foco principal estuvo en asegurar que el motor fuera robusto y no fallara. 

### Lo que hice concretamente:
- **Suite de Pruebas:** Desarrollé una serie de tests unitarios que cubren el **97% del código**. Mi meta fue que cualquier cambio en la lógica (como el algoritmo de expansión o el cálculo de minas) pudiera verificarse al instante.
- **Validación de Algoritmos:** Me encargué de testear que el sistema de descubrimiento de celdas (BFS) y el cálculo de minas adyacentes funcionen correctamente en distintos tamaños de tablero.
- **Persistencia de Datos:** Trabajé en las funciones de carga y guardado de partidas, asegurando que el sistema valide correctamente los archivos externos y no se rompa si los datos vienen mal formateados.

## 🛠️ Herramientas usadas
- **Python 3.12+**
- **Unittest:** Para la automatización de las pruebas.
- **Coverage.py:** Para medir qué tanto del código está realmente cubierto por los tests.

## ⚙️ Cómo correr los tests
Si tenés Python instalado, podés verificar la integridad del motor ejecutando:
```bash
python -m unittest tests.py
