title: Experimentando con Flask Parte 1
date: 2020-10-31
tags: flask, web development, python
summary: Este articulo es el inicio de una serie en la cual aprenderemos Flask con algo de Python, la instalación del mismo en una instancia o Cloud Server en Rackspace Technology. Finalizaremos con algunas recomendaciones las cuales incluirán actualizaciones automáticas mediante gitup, edición y editores de Markdown entre otros temas.
author: Alberto Ferrer

## Introducción

Este articulo es el inicio de una serie en la cual aprenderemos Flask con algo de Python, la instalación del mismo en una instancia o Cloud Server en Rackspace Technology. Finalizaremos con algunas recomendaciones las cuales incluirán actualizaciones automáticas mediante gitup, edición y editores de Markdown entre otros temas.

Artículos de esta serie:

1. Introducción a Flask (este artículo)
2. [Instalación en un Cloud Server](</article/experimentando-con-flask-parte-2>)
3. [Actualizaciones automáticas](</article/experimentando-con-flask-parte-3>)

## Comenzando con Flask

Flask es un framework o conjunto de librerías en Python el cual ayuda al desarrollo web, es amigable, simple de utilizar y estable. Como todo framework, la seguridad depende de la implementación y el desarrollador.  

Dependiendo de como decidamos comenzar, instalar Flask es bastante rápido y simple:

```bash
pip3 install flask --user
```

Con la siguiente linea hemos instalado Flask en nuestra carpeta de usuario, para nuestros fines esto sera suficiente.

## Nuestra primera aplicación en Flask

Ahora crearemos un archivo cualquiera, el cual tendrá la extensión de ".py" y agregaremos el siguiente código:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

Luego ejecutaremos la aplicación de la siguiente forma:

```bash
$ export FLASK_APP=hello.py
$ flask run
 * Running on http://127.0.0.1:5000/
```

Si quieren mas información sobre Flask y la documentación del mismo les recomiendo visitar [Quickstart &#8212; Flask Documentation (1.1.x)](https://flask.palletsprojects.com/en/1.1.x/quickstart/).

## Agregando templates a nuestra aplicación

Una de las maravillas de Flask es la fácil y rápida aplicación de templates o diseños utilizando herencia. 

Un ejemplo sencillo de esto seria:

```python
@app.route('/')
def home():
    return render_template('home.html')
```

Mas información de esto se puede encontrar en "Rendering Templates" en el enlace que les deje arriba.

Como podrán leer, la creación básica de un sitio estático en Flask es sencilla, rápida y amigable.

Para fines descriptivos esta entrada es mas que suficiente, ahora vamos a obtener el código de una aplicación de ejemplo la cual he armado y estaremos utilizando. 

```bash
git clone https://github.com/bet0x/barrahome-flask
```

Para instalar los paquetes y requerimientos de este articulo ejecutaremos pip con la siguiente sentencia: 

```bash
pip3 install -r requeriments.txt
```

Luego ejecutaremos nuestra aplicación con:

```bash
python3 run.py
```

He ingresaremos a la dirección señalada en nuestra consola:

```bash
 * Serving Flask app "website" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 212-996-953
```