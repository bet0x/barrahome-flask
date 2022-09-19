title: post-merge con Python en Linux
date: 2022-09-19
tags: post-merge, git, systemd, python, linux, gitup
summary: Actualizando mi blog con Github, Gitup via post-merge con un backend en Flask (Python) en Linux. (TLTR)
author: Alberto Ferrer

Voy a utilizar y modificar la siguiente implementación para el hook de [post-merge](https://git-scm.com/docs/githooks#_post_merge) en git. 

```bash
#!/usr/bin/env bash
# MIT © Sindre Sorhus - sindresorhus.com

# git hook to run a command after `git pull` if a specified file was changed
# Run `chmod +x post-merge` to make it executable then put it into `.git/hooks/`.

changed_files="$(git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD)"

check_run() {
	echo "$changed_files" | grep --quiet "$1" && eval "$2"
}

# Example usage
# In this example it's used to run `npm install` if package.json changed
check_run *website/content* "systemctl reload barrahome"
```

La lógica detrás de mi aplicación de Blog es la siguiente:

Escribo un articuló y queda publicado **/website/content** luego de 5 minutos el servidor ejecuta gitup, si existe alguna actualización, esta es descargada y se debería ejecutar un reload del blog, este va mediante lo descrito [aquí](https://www.barrahome.org/article/gunicorn-reload-systemd). 

Como mi frontend es Nginx, tengo que *de vez en cuando* limpiar su cache, esto se realizara mediante un key el cual se implementa de la siguiente forma:

```bash
proxy_cache_bypass $http_palabra_secreta;
```

Luego simplemente ejecuto: 
```bash
[alberto@barrahome ~]$ curl https://www.barrahome.org/ -s -I -H "palabra_secreta:true"|grep x-cache-status
x-cache-status: BYPASS
[alberto@barrahome ~]$
```
Esto se puede proteger mediante un location y una restricción de IP. Se puede cambiar la URL y reflejar la pagina cual vamos a renovar. 

Elementos los cuales debería verificar luego de que se ejecuta gitup:

* Cambie código en la aplicación barrahome.py
* Cambie, agregue o modifique un template.