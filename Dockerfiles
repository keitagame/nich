
FROM richarvey/nginx-php-fpm:2.1.2

COPY . .

ENV WEBROOT /var/www/html
ENV PHP_ERRORS_STDERR 1
ENV RUN_SCRIPTS 1

CMD ["/start.sh"]
