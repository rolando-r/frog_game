# Frog Jump Game 🐸🍃

Este es un juego de una rana que salta sobre hojas e intenta escapar de sus enemigos.

## Descripción
- Controlas una rana que salta hacia adelante.
- Debes aterrizar sobre hojas flotantes; si fallas, pierdes.
- Hay dos tipos de enemigos ellos son pajaros que te quieren atrapar y serpientes que no puedes pisar.
- El juego incluye menú de inicio y fin de juego.

## Estructura 📁
- `src/`: Código fuente en Python.
- `assets/images`: Imágenes de sprites.
- `assets/sounds`: Efectos de sonido.

## Instrucciones para jugar 🛠️
1. Clonar este repositorio.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
3. Ejecutar:
    ```bash
   cd src
4. Ejecutar:
    ```bash
   python main.py

Si no tienes instalado PIP, revisa la documentación oficial para instalarlo:
https://pip.pypa.io/en/stable/installation/

## Controles 🎮
- `Enter`: Seleccionar (Menú).
- `Espacio`: Hacer que la rana salte.
- `A o ←`: Mover la rana hacía la izquierda.
- `D o →`: Mover la rana hacía la derecha.

## Buenas practicas ✨
- Organización en módulos y funciones reutilizables.
- Clases para entidades principales: Frog, Enemy, Bird, Snake.
- Uso de constantes en `utils.py`.
