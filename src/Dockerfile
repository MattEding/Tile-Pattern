FROM heroku/miniconda

ADD ./tileapp /opt/tileapp/
WORKDIR /opt/tileapp

ADD ./tileapp/requirements.txt /tmp/requirements.txt
RUN conda install --file /tmprequirements.txt

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
