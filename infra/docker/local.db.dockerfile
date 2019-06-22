# Dockerfile for use in my local environment for the MySQL database
# Author: Andrew Jarombek
# Date: 6/22/2019

FROM mysql:5.7

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile for the SaintsXCTF MySQL database for local development"

EXPOSE 3306 33060
CMD ["mysqld"]