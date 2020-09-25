# Dockerfile for an Nginx reverse proxy to the Flask API in production.
# Author: Andrew Jarombek
# Date: 9/20/2020

FROM nginx:latest

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile for the Nginx Reverse Proxy to the SaintsXCTF API in Production"

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

STOPSIGNAL SIGTERM
EXPOSE 80