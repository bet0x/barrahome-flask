title: Gunicorn reload Systemd
date: 2022-09-18
tags: gunicorn, systemd
summary: Recargar la configuración o cambios de Gunicorn mediante Systemd.
author: Alberto Ferrer

Se agregan estas las lineas **ExecReload** y **ExecStop** al "unit" de systemd.

El [siguiente](https://www.barrahome.org/article/gunicorn-flask-systemd) articulo describe la utilización y otros temas:


```bash
[alberto@barrahome barrahome-flask]$ cat /etc/systemd/system/barrahome.service
[Unit]
Description=Barrahome web application
After=network.target

[Service]
User=alberto
Group=alberto
WorkingDirectory=/home/alberto/barrahome-flask
ExecStart=/usr/bin/python3 /usr/bin/gunicorn  --bind 127.0.0.1:8000 website:app --pid=barrahome.pid
ExecReload = /bin/kill -s HUP $MAINPID
ExecStop = /bin/kill -s TERM $MAINPID

[Install]
WantedBy=multi-user.target
[alberto@barrahome barrahome-flask]$
```
Luego ejecutamos:
```bash
[alberto@barrahome barrahome-flask]$ sudo systemctl daemon-reload
[alberto@barrahome barrahome-flask]$ sudo systemctl reload barrahome
```

Verificamos si se ejecuto:
```bash
[alberto@barrahome barrahome-flask]$ sudo systemctl status barrahome
● barrahome.service - Barrahome web application
   Loaded: loaded (/etc/systemd/system/barrahome.service; enabled; vendor preset: disabled)
   Active: active (running) since Sun 2022-09-18 23:06:14 UTC; 13min ago
 Main PID: 26783 (python3)
    Tasks: 2 (limit: 24844)
   Memory: 35.4M
   CGroup: /system.slice/barrahome.service
           ├─26783 /usr/bin/python3 /usr/bin/gunicorn --bind 127.0.0.1:8000 website:app --pid=barrahome.pid
           └─26849 /usr/bin/python3 /usr/bin/gunicorn --bind 127.0.0.1:8000 website:app --pid=barrahome.pid

Sep 18 23:06:14 barrahome python3[26783]: [2022-09-18 23:06:14 +0000] [26783] [INFO] Starting gunicorn 20.0.4
Sep 18 23:06:14 barrahome python3[26783]: [2022-09-18 23:06:14 +0000] [26783] [INFO] Listening at: http://127.0.0.1:8000 (26783)
Sep 18 23:06:14 barrahome python3[26783]: [2022-09-18 23:06:14 +0000] [26783] [INFO] Using worker: sync
Sep 18 23:06:14 barrahome python3[26788]: [2022-09-18 23:06:14 +0000] [26788] [INFO] Booting worker with pid: 26788
Sep 18 23:08:06 barrahome systemd[1]: Reloading Barrahome web application.
Sep 18 23:08:06 barrahome python3[26783]: [2022-09-18 23:08:06 +0000] [26783] [INFO] Handling signal: hup
Sep 18 23:08:06 barrahome python3[26783]: [2022-09-18 23:08:06 +0000] [26783] [INFO] Hang up: Master
Sep 18 23:08:06 barrahome systemd[1]: Reloaded Barrahome web application.
Sep 18 23:08:06 barrahome python3[26788]: [2022-09-18 23:08:06 +0000] [26788] [INFO] Worker exiting (pid: 26788)
Sep 18 23:08:06 barrahome python3[26849]: [2022-09-18 23:08:06 +0000] [26849] [INFO] Booting worker with pid: 26849
[alberto@barrahome barrahome-flask]$
```
