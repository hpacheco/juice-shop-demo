FROM node:19
COPY . /juice-shop
WORKDIR /juice-shop
RUN npm install
RUN apt update && apt install -y systemctl apache2 php libapache2-mod-php php-mysql
RUN a2enmod mpm_prefork && a2enmod php7.4
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_RUN_DIR /var/www/html
RUN echo 'Hello, docker' > /var/www/index.html
COPY shake-logger/shake.js shake-logger/logger.php /var/www/html/
EXPOSE 3000
EXPOSE 80
ENV NODE_ENV=unsafe
ENV TARGET_SOCKET=localhost:8080
RUN echo "#! /bin/bash" >> ./startup.sh
RUN echo "service apache2 restart" >> ./startup.sh
RUN echo "node /juice-shop/build/app.js" >> ./startup.sh
CMD ["/bin/bash","-c","./startup.sh"]