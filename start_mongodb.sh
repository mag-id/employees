#!/bin/bash
docker run \
    --name db \
    -e MONGO_INITDB_ROOT_USERNAME=username \
    -e MONGO_INITDB_ROOT_PASSWORD=password \
    -p 27017:27017 \
mongo:5.0.12
