title: Notificacion de Login/Logout en conexiones SSH
date: 2010-01-14
tags: bash, ssh, seguridad
summary: Aunque se que no es muy seguro puesto puede ser borrado nos notificara antes que se realice tal evento.
author: Alberto Ferrer

Vamos a editar 2 archivos, el primero sera .bash_profile el cual nos notificara cuando ingresa al sistema la persona:

Debajo del primer comentario agregamos lo siguiente:

```bash
echo 'ALERT - Root Shell Access on:' `date` `who` | mail -s "Alert: Root Access from `who | awk '{print $6}'`" mi@email.com
```

Reemplazamos mi@email.com con el email el cual recibirá la alerta.

Ahora hacemos lo mismo con .bash_logout y agregamos lo siguiente:

```bash
echo 'ALERT - Root Shell Logout on:' `date` `who` | mail -s "Alert: Root Logout from `who | awk '{print $6}'`" mi@email.com
```

Con esto el servidor nos advertirá ante cualquier ingreso o salida del sistema. Debemos tener por seguro que este metodo puede ser saltado. 