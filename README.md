the docker instance will run with the folowing mappings:
"./site" maps to "/opt/www" \
"./site-python" maps to "/opt/python"

"/opt/python" is automatically added to the python path.

the mapping below allows the instance to access your local mysql install.
"/run/mysqld/mysqld.sock" maps to "/run/mysqld/mysqld.sock"

Edit run_sample.sh as required.
![Screenshot](https://i.ibb.co/z6fBbdN/Screenshot-from-2021-03-02-08-14-56.png)
