title: Gunicorn , Flask y Systemd
date: 2020-11-05
tags: gunicorn, flask, systemd
summary: Simple instalacion de Gunicorn utilizando Systemd
author: Alberto Ferrer

## Introducción

Creamos un servicio, en este caso se llamara como mi blog.

```bash
[alberto@barrahome barrahome-flask]$ sudo nano /etc/systemd/system/barrahome.service
```
Agregamos el siguiente contenido:

```bash
[Unit]
Description=Barrahome web application
After=network.target

[Service]
User=alberto
Group=alberto
WorkingDirectory=/home/alberto/barrahome-flask
ExecStart=/usr/bin/python3 /usr/bin/gunicorn --bind 0.0.0.0:8000 boot:app

[Install]
WantedBy=multi-user.target
```

Habilitamos el servicio y luego recargamos systemd y sus servicios:

```bash
[alberto@barrahome barrahome-flask]$ sudo systemctl daemon-reload
[alberto@barrahome barrahome-flask]$ sudo systemctl start barrahome
[alberto@barrahome barrahome-flask]$ sudo systemctl status barrahome
● barrahome.service - Barrahome web application
   Loaded: loaded (/etc/systemd/system/barrahome.service; enabled; vendor preset: disabled)
   Active: active (running) since Thu 2020-11-05 22:40:37 UTC; 52s ago
 Main PID: 54217 (python3)
    Tasks: 2 (limit: 23957)
   Memory: 34.0M
   CGroup: /system.slice/barrahome.service
           ├─54217 /usr/bin/python3 /usr/bin/gunicorn --bind 0.0.0.0:8000 boot:app
           └─54220 /usr/bin/python3 /usr/bin/gunicorn --bind 0.0.0.0:8000 boot:app

Nov 05 22:40:37 barrahome systemd[1]: Started Barrahome web application.
Nov 05 22:40:37 barrahome python3[54217]: [2020-11-05 22:40:37 +0000] [54217] [INFO] Starting gunicorn 20.0.4
Nov 05 22:40:37 barrahome python3[54217]: [2020-11-05 22:40:37 +0000] [54217] [INFO] Listening at: http://0.0.0.0:8000 (54217)
Nov 05 22:40:37 barrahome python3[54217]: [2020-11-05 22:40:37 +0000] [54217] [INFO] Using worker: sync
Nov 05 22:40:37 barrahome python3[54217]: [2020-11-05 22:40:37 +0000] [54220] [INFO] Booting worker with pid: 54220
[alberto@barrahome barrahome-flask]$
```
