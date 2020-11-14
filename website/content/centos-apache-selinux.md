title: Centos Apache SELinux
date: 2020-11-15
tags: centos, apache, selinux
summary: Guía rápida de como habilitar SELinux con Apache en Centos 7/8 utilizando directorio personal y otros características.
author: Alberto Ferrer

Esto es ciertamente muy básico pero útil y practico. Tener en cuenta que hay pasos los cuales me salte dado que cualquiera leyendo esto tiene una noción básica de lo que estoy escribiendo.

Luego de instalar Apache con dnf o yum pasamos a permitir Apache con el siguiente comando:

```bash
sudo setsebool -P httpd_can_network_connect 1
sudo setsebool -P httpd_enable_homedirs 1
```

Si quieren saber que otras opciones existen en el contexto de httpd pueden ejecutar esta variante:

```bash
sudo getsebool -a | grep "httpd_can"
```

Luego procedemos a crear nuestro directorio:

```bash
mkdir public_html
chmod 0755 public_html
```

En el caso de que se requiera hacer operaciones de lectura/escritura debemos permitir nuestra carpeta con este otro comando:

```bash
chcon -Rv --type=httpd_sys_rw_content_t /home/usuario/public_html
```

En el caso de que busquemos solo lectura (servir archivos y no nos funcione nuestro public_html):

```bash
chcon -t httpd_sys_content_t /home/usuario/public_html
```

Creamos nuestro vhost:

```bash
sudo vim /etc/httpd/sites-available/barrahome.org.conf
<VirtualHost *:80>
    ServerName barrahome.org
    ServerAlias barrahome.org www.barrahome.org
    DocumentRoot /home/usuario/public_html
    ErrorLog /home/usuario/logs/error.log
    CustomLog /home/usuario/logs/custom.log combined
</VirtualHost>
sudo ln -s /etc/httpd/sites-available/barrahome.org.conf /etc/httpd/sites-enabled/barrahome.org.conf
```

Ahora permitiremos a Apache la escritura de logs en nuestro directorio personal:

```bash
sudo semanage fcontext -a -t httpd_log_t "/home/usuario/logs(/.*)?"
```

Para finalizar aplicamos los cambios:

```bash
sudo restorecon -R -v /home/usuario/public_html
sudo restorecon -R -v /home/usuario/logs
```