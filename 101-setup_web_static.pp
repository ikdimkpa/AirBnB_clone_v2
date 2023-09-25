# a puppet manifest that sets up your web servers for the deployment of web_static

$STATIC_CONFIG='\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t\tindex index.html index.htm;\n\t}'
$STATIC_COMMENT='\t# Serve static content'
$ERROR_COMMENT='\t# Custom error page'
$CUSTOM_ERROR='\terror_page 404 /custom_404.html;\n\tlocation = /custom404.html {\n\t\troot /var/www/html;\n\t\tinternal;\n\t}'

package { 'nginx':
  ensure => installed,
}

-> file_line { 'redirect_me':
  ensure => 'present',
  path   => '/etc/nginx/sites-available/default',
  after  => 'listen 80 default_server;',
  line   => 'rewrite ^/redirect_me/?$ https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;',
}

-> file_line { 'custom_header':
  ensure => 'present',
  path   => '/etc/nginx/sites-available/default',
  after  => 'listen 80 default_server;',
  line   => 'add_header X-Served-By 6684-web-01;',
}

-> exec { 'static_config'
  path    => '/usr/bin:/bin',
  command => 'sudo sed -i "/server_name _/a\\\n$STATIC_COMMENT\n$STATIC_CONFIG" /etc/nginx/sites-available/default'
}

-> exec { 'custom_error'
  path    => '/usr/bin:/bin',
  command => 'sudo sed -i "/server_name _;/a\\\n\n$ERROR_COMMENT\n$CUSTOM_ERROR" /etc/nginx/sites-available/default'
}

-> file { '/data':
  ensure  => 'directory'
}

-> file { '/data/web_static':
  ensure => 'directory'
}

-> file { '/data/web_static/releases':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test':
  ensure => 'directory'
}

-> file { '/data/web_static/shared':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "this webpage is found in data/web_static/releases/test/index.htm \n"
}

-> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
}

-> exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

-> file { 'home_page':
  path    => '/var/www/html/index.html',
  content => 'Hello World!',
}

-> service { 'nginx':
  ensure  => running,
  require => Package['nginx'],
}
