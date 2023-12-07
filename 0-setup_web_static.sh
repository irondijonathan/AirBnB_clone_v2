#!/usr/bin/env bash
#Sets up web servers for the deployment of web_static

folders=("/data/" "/data/web_static/" "/data/web_static/releases/" "/data/web_static/shared/" "/data/web_static/releases/test/")
SERVER_CONFIG=\
"server {
	listen 80 default_server;
	listen [::]:80 default_server;

	server_name _;
  index index.html index.htm;
	error_page 404 /404.html;

  location / {
    root /var/www/html/;
		try_files \$uri \$uri/ =404;
	}

	location /hbnb_static/ {
		alias /data/web_static/current/;
	}
}"
PAGE=\
"<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
"

apt-get -y update
apt-get -y install nginx
ufw allow 'Nginx HTTP'

for folder in "${folders[@]}"
do
    if [ ! -d "${folder}" ]; then
        mkdir "${folder}"
    fi
done

echo "$PAGE" | tee "/data/web_static/releases/test/index.html"

if [ -L "/data/web_static/current" ]; then
    rm "/data/web_static/current"
fi
ln -s "/data/web_static/releases/test/" "/data/web_static/current"

echo "$SERVER_CONFIG" > /etc/nginx/sites-enabled/default

chown -R ubuntu:ubuntu "/data/"

if [ "$(pgrep -c nginx)" -le 0 ]; then
	service nginx start
else
	service nginx restart
fi
