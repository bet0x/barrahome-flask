title: Gunicorn reload Systemd
date: 2022-09-18
tags: gunicorn, systemd
summary: Recargar la configuración o cambios de Gunicorn mediante Systemd.
author: Alberto Ferrer

Se agregan estas las lineas **ExecReload** y **ExecStop** al "unit" de systemd creado para Gunicorn [leer](https://www.barrahome.org/article/gunicorn-flask-systemd):

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