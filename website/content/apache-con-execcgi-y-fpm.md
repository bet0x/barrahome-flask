title: Apache con ExecCGI y FPM
date: 2022-09-22
tags: apache, execcgi, fpm
summary: Una simple receta con notas de como se debe configurar un Virtual Host con Apache para que ejecute CGIs y PHP.
author: Alberto Ferrer

Esta configuración de Apache se realizo bajo Ubuntu 22.04 con el modulo de proxy_fcgi, setenvif y cgid. Estos módulos se deben habilitar si nuestro MPM es **event**, esto se puede verificar mediante:

```bash
sudo apachectl status |grep -i 'Server MPM:'
```

La configuración para Apache sera la siguiente:

```bash
<VirtualHost *:80>
    ServerAdmin alberto@localhost.barrahome.org
    ServerName localhost.barrahome.org
    DocumentRoot /home/alberto/public_html
    DirectoryIndex index.php index.html
    ErrorLog ${APACHE_LOG_DIR}/error-localhost.barrahome.org.log
    CustomLog ${APACHE_LOG_DIR}/access-localhost.barrahome.org.log combined

<Directory />
   Options -FollowSymLinks +SymLinksIfOwnerMatch
   AllowOverride All
   Require all granted
</Directory>

<FilesMatch \.php$>
   SetHandler "proxy:unix:/run/php/localhost.barrahome.org.sock|fcgi://localhost/"
</FilesMatch>

<IfModule mod_alias.c>
        <IfModule mod_cgi.c>
                Define ENABLE_USR_LIB_CGI_BIN
        </IfModule>

        <IfModule mod_cgid.c>
                Define ENABLE_USR_LIB_CGI_BIN
        </IfModule>

        <IfDefine ENABLE_USR_LIB_CGI_BIN>
                ScriptAlias /cgi-bin/ /home/alberto/public_html/cgi-bin/
                <Directory "/home/alberto/public_html/cgi-bin/">
                        AllowOverride None
                        Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
                        Require all granted
                </Directory>
        </IfDefine>
</IfModule>

</VirtualHost>
```

Tengan en cuenta que estoy utilizando PHP-FPM con un pool dedicado **localhost.barrahome.org.sock**. Los permisos para /home y para /home/alberto son de ejecución. 

Aquí el script de Perl el cual he creado para la prueba:

```perl
#!/usr/bin/perl
use strict;
use warnings;

print "Content-type: text/html\n\n";
print "Hello World";

print "<pre>\n";
my $key;
foreach $key (sort keys(%ENV)){
   print "$key = $ENV{$key}<p>";
}
print "</pre>";
```

Algo importante, se puede aplicar **+ExecCGI** directamente a **/home/alberto/public_html** y evitar tener que utilizar **cgi-bin**. 

**NOTA:** Quiero destacar que utilizar **SymLinksIfOwnerMatch** en el caso de ser requerido ayuda también a prevenir ataques del tipo **[Symlink Attack](https://capec.mitre.org/data/definitions/132.html)**. En PHP esto se previne mediante la configuración del valor **[open_basedir](https://www.php.net/manual/en/ini.core.php)**. 
