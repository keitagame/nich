FROM debian:stable-slim


RUN apt-get update && \
    apt-get install -y nginx fcgiwrap spawn-fcgi perl libcgi-pm-perl libencode-japanese-perl && \
    apt-get clean

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY . /var/www/html
RUN chmod -R 755 /var/www/html/test/bbs.cgi
CMD spawn-fcgi -s /var/run/fcgiwrap.socket -M 766 /usr/sbin/fcgiwrap && \
    nginx -g "daemon off;"
