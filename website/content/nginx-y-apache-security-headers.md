title: Nginx y Apache Security Headers
date: 2022-10-05
tags: apache, nginx, security, headers
summary: Security Headers para Apache y Nginx actualizados, una breve reseña de los mismos. 
author: Alberto Ferrer

Este breve articulo no es mas que una nota o cheatsheet de los security headers a utilizar y requeridos en su mayoría. Si desean leer sobre el tema pueden seguir el [siguiente enlace.](https://owasp.org/www-project-secure-headers/)

```bash
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Permitted-Cross-Domain-Policies "none" always;
add_header Feature-Policy "microphone none;camera none;geolocation none;";
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src * data: 'unsafe-eval' 'unsafe-inline'" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header Expect-CT "max-age=31536000; report-uri=https://www.barrahome.org/contact";
add_header Access-Control-Allow-Origin "*" always;
```

El equivalente para Apache seria utilizando algo como esto:

```bash
<IfModule mod_headers.c>
   Header set header-Name: Values
<IfModule mod_headers.c>
```
