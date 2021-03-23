FROM nginx:1.19.8

ARG NGINX_UPSTREAM
ENV NGINX_UPSTREAM $NGINX_UPSTREAM

COPY nginx.conf /etc/nginx/
COPY voyages.conf /etc/nginx/conf.d/
RUN sed -ie 's/voyages-django:8000/'"$NGINX_UPSTREAM"':8000/' /etc/nginx/conf.d/voyages.conf

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]
