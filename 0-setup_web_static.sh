#!/usr/bin/env bash
# a Bash script that sets up your web servers for the deployment of web_static

# install nginx if not installed
if ! nginx -v &> /dev/null; then
	sudo apt-get update -y
	sudo apt-get install -y nginx
fi

# Create the folder /data/ if it doesn’t already exist
if [[ ! (-e /data/web_static && -d /data/web_static) ]]; then
	sudo rm -rf /data
	sudo mkdir -p /data
fi

# Create the folder /data/web_static/ if it doesn’t already exist
if [[ ! (-e /data/web_static && -d /data/web_static) ]]; then
	sudo rm -rf /data/web_static
	sudo mkdir -p /data/web_static
fi

# Create the folder /data/web_static/releases/ if it doesn’t already exist
if [[ ! (-e /data/web_static/releases && -d /data/web_static/releases) ]]; then
	sudo rm -rf /data/web_static/releases
	sudo mkdir -p /data/web_static/releases
fi

# Create the folder /data/web_static/shared/ if it doesn’t already exist
if [[ ! (-e /data/web_static/shared && -d /data/web_static/shared) ]]; then
	sudo rm -rf /data/web_static/shared
	sudo mkdir -p /data/web_static/shared
fi

# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
if [[ ! (-e /data/web_static/releases/test && -d /data/web_static/releases/test) ]]; then
	sudo rm -rf /data/web_static/releases/test
	sudo mkdir -p /data/web_static/releases/test
fi

# Create a fake HTML file /data/web_static/releases/test/index.html
# (with simple content, to test your Nginx configuration)
if [[ -e /data/web_static/releases/test/index.html ]]; then
	sudo rm -rf /data/web_static/releases/test/index.html
fi
echo -e "<!DOCTYPE html>
<html lang=\"en\">
	<head><meta charset=\"utf-8\"></head
	<body>Holberton School</body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder.
# If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). 
# This should be recursive; everything inside should be created/owned by this user/group.
sudo chown -R ubuntu:ubuntu /data/

# Configure nginx
echo "Hello World!" | sudo tee /var/www/html/index.html > /dev/null # create a file with the text Hello World!
echo "Ceci n'est pas une page" | sudo tee /var/www/html/custom_404.html > /dev/null # create the error page file

if ! grep "# Permanent redirect" /etc/nginx/sites-available/default &> /dev/null ; then
	COMMENT='\t# Permanent redirect'
	REDIRECT='\trewrite ^/redirect_me/?$ https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;'
	sudo sed -i "/server_name _;/a\\\n\n$COMMENT\n$REDIRECT" /etc/nginx/sites-available/default
fi

if ! grep "# Custom error page" /etc/nginx/sites-available/default &> /dev/null ; then
	ERROR_COMMENT='\t# Custom error page'
	CUSTOM_ERROR='\terror_page 404 /custom_404.html;\n\tlocation = /custom404.html {\n\t\troot /var/www/html;\n\t\tinternal;\n\t}'
	sudo sed -i "/server_name _;/a\\\n\n$ERROR_COMMENT\n$CUSTOM_ERROR" /etc/nginx/sites-available/default
fi

if ! grep "# Custom header" /etc/nginx/sites-available/default &> /dev/null; then
	HEADER_COMMENT='\t# Custom header'
	CUSTOM_HEADER='\tadd_header X-Served-By'
	sudo sed -i "/server_name _/a\\\n\n$HEADER_COMMENT\n$CUSTOM_HEADER $HOSTNAME;" /etc/nginx/sites-available/default
fi

if ! grep "# Serve static content" /etc/nginx/sites-available/default &> /dev/null; then
	STATIC_COMMENT='\t# Serve static content'
	STATIC_CONFIG='\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t\tindex index.html index.htm;\n\t}'
	sudo sed -i "/server_name _/a\\\n$STATIC_COMMENT\n$STATIC_CONFIG" /etc/nginx/sites-available/default
fi

sudo service nginx restart # start the server if not already started
