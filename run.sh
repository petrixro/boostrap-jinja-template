#!/bin/bash
docker run -p 5000:5000 \
    -v "${PWD}/Website/site:/opt/www" \
    -v "${PWD}/Website/site-python:/opt/site-python" \
    -v "${HOME}/dev/python:/opt/python" \
    flask-framework
    
