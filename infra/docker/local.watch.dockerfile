# Dockerfile for use in my local environment for watching changes to local code and placing in a volume
# Author: Andrew Jarombek
# Date: 6/23/2019

FROM alpine

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile for a container that watches the SaintsXCTF API for changes in local development"