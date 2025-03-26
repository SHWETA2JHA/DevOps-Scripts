#!/bin/bash

DOMAIN="yourdomain.com"
EMAIL="youremail@example.com"

echo "Updating system and installing Nginx."
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y nginx

echo "Configuring firewall."
sudo ufw allow 'Nginx Full'
sudo ufw enable

echo "Installing Certbot."
sudo apt install -y certbot python3-certbot-nginx

echo "Obtaining SSL certificate from Let's Encrypt."
sudo certbot --nginx --non-interactive --agree-tos --email $EMAIL -d $DOMAIN

if sudo certbot certificates | grep -q "$DOMAIN"; then
    echo "SSL certificate installed successfully!"
else
    echo "SSL certificate installation failed!"
    exit 1
fi

echo "Configuring automatic certificate renewal."
echo "0 3 * * * root certbot renew --quiet" | sudo tee -a /etc/crontab > /dev/null

echo "Restarting Nginx."
sudo systemctl restart nginx

echo "Nginx with SSL has been set up successfully!"
