# Mercado Libre Challenge
Date: 15-03-2021

## Resumen
crear un autocompletado para empleados del área de experiencia de usuarios basado en datos de ejemplo.

### Modelo implementado
offline
- limpieza de texto
- obtención de oraciones más frecuentes
- modelo de similaridad de oraciones utilizando transformers con modelos pre-entrenados que analizan el significado además de coincidencias semánticas. Esto se realiza para evitar recomendar oraciones parecidas.

online
- obtencion de las oraciones mas frecunetes que coincidan y eliminacion de oraciones parecidas

## instalación
### entorno virtual
Para la ejecución completa del proyecto, se recomienda un entorno virtual con pytorch que dependiendo el sistema operativo puede haber variaciones para su instalación. 

1) linux:

```bash
pip install -r requirements.txt
```

2) otro:
Para otros OS se puede consultar como cambiar los comandos desde la página oficial de [pytorch](https://pytorch.org/get-started/locally/#start-locally) o utilizar el requirements sin pytorch y utilizar el modelo ya entrenado que se encuentra en la carpeta `modelo`.

3) docker + opción 1

4) sin pytorch (no se podrá compilar)
    - copiar el modelo que se encuntra en `./modelo/autocompleter.pkl` a `.`
    ```bash
    cp ./modelo/autocompleter.pkl .
    pip install -r requirements_sin_pytorch.txt
    ```

### ejecución del proyecto
- una vez creado el ambiente de trabajo:

```bash
python autocompleter_build.py
python autocompleter_server.py
```


__NOTA:__ si es la primera vez que se va a compilar, se baja el modelo y puede tardar unos minutos. Si ya se ha bajado, a partir de la segunda compilación del autocompleter en adelante es muy rápida.


- si se quieren ejecutar los tests realizados de comprobación:
```bash
pytest -v
```

## Comentarios generales sobre el proyecto
### Objeto Autocompleter
Se han agregado algunos métodos para ir probando distintos modelos y reaprovechar el código. Por este motivo, la clase quedó con algunos pocos métodos más que el framework entregado.

### Versiones
Se han realizado pruebas para probar distintos autocompletados. Las mismas se han realizado en jupyter-notebook para decidir cual elegir y pasar al framework entregado. Algunas pruebas sencillas se pueden ver en notebooks dentro de la carpeta `./pruebas_para_otras_versiones/`






