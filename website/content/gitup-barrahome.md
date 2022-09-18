title: Gitup Barrahome
date: 2022-09-18
tags: gitup, python, barrahome
summary: Guía rápida de como utilizar Gitup para actualizar mi blog automáticamente. 
author: Alberto Ferrer

Instalamos Gitup:

```bash
sudo pip3 install gitup
```

Habilitamos el repositorio el cual actualizaremos:

```bash
gitup --add ~/barrahome-flask
```

Creamos una entrada de cron:

```bash
crontad -e
```

Agregamos la siguiente entrada:

```bash
*/5 * * * * gitup --update
```

Si deseamos listar los repositorios que tenemos para actualizar podemos ejecutar lo siguiente:

```bash
gitup --list
```

Nos dara como salida algo como esto:

```bash
[alberto@barrahome barrahome-flask]$ gitup --list
gitup: the git-repo-updater

Current bookmarks:
    /home/alberto/barrahome-flask
[alberto@barrahome barrahome-flask]$
```