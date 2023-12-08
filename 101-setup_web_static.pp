#!/usr/bin/puppet apply
# Puppet: Sets up web servers for the deployment of web_static
exec { 'apt-get-update':
  command => '/usr/bin/apt-get update',
  path    => '/usr/bin:/usr/sbin:/bin',
}

exec { 'remove-current':
  command => 'rm -rf /data/web_static/current',
  path    => '/usr/bin:/usr/sbin:/bin',
}

package { 'nginx':
  ensure  => installed,
  require => Exec['apt-get-update'],
}

file { '/var/www':
  ensure  => directory,
  mode    => '0755',
  recurse => true,
  require => Package['nginx'],
}

exec { 'make-static-files-folder':
  command => 'mkdir -p /data/web_static/releases/test /data/web_static/shared',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => Package['nginx'],
}

file { '/data/web_static/releases/test/index.html':
  content =>
"<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
",
  replace => true,
  require => Exec['make-static-files-folder'],
}

exec { 'link-static-files':
  command => 'ln -sf /data/web_static/releases/test/ /data/web_static/current',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => [
    Exec['remove-current'],
    File['/data/web_static/releases/test/index.html'],
  ],
}

exec { 'change-data-owner':
  command => 'chown -hR ubuntu:ubuntu /data',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => Exec['link-static-files'],
}

file { '/etc/nginx/sites-available/default':
  ensure  => present,
  mode    => '0644',
  content =>
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
}",

require => [
    Package['nginx'],
    Exec['change-data-owner']
  ],
}

exec { 'enable-site':
  command => "ln -sf '/etc/nginx/sites-available/default' '/etc/nginx/sites-enabled/default'",
  path    => '/usr/bin:/usr/sbin:/bin',
  require => File['/etc/nginx/sites-available/default'],
}

exec { 'start-nginx':
  command => 'sudo service nginx restart',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => [
    Exec['enable-site'],
    Package['nginx'],
    File['/data/web_static/releases/test/index.html'],
  ],
}

Exec['start-nginx']