#!/bin/bash
docker run -p 5000:5000 \
    --net=host \
    -it \
    -v "${PWD}/Website/site:/opt/www" \
    -v "${HOME}/dev/python:/opt/python" \
    flask-py3-google-api \
   /bin/bash
