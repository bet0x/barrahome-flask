title: Evitando XSS, ClickJacking Attacks y otras cosas en PHP
date: 2012-12-04
tags: php, seguridad
summary: Buscando evitar XSS, ClickJacking me puse a mirar notas de seguridad para php y así mejorar mi blog mientras desarrollo mi proyecto sobre clusters en nginx aplique estos arreglos que mejoran la seguridad en mi wordpress y mis otros proyectos basados en php.
author: Alberto Ferrer

### Prevenir XSS:

http://people.mozilla.org/~bsterne/content-security-policy/index.html

```
header("X-Content-Security-Policy: allow 'self'; frame-ancestors 'none'");
header("X-XSS-Protection: '1'; mode='block'");
```

### Prevenir ClickJacking:

http://es.wikipedia.org/wiki/Clickjacking

```
header('X-Frame-Options: DENY');
```

### Prevenir que Internet Explorer adivine el Content-Type:

http://blogs.msdn.com/ie/archive/2008/07/02/ie8-security-part-v-comprehensive-protection.aspx

```
header('X-Content-Type-Options: nosniff' );
```

Prometo ir adentrando en estos temas mas adelante y así armarles una seguidilla de artículos prácticos para todos.