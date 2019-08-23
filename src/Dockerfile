FROM heroku/miniconda

ADD ./tileapp /opt/tileapp/
WORKDIR /opt/tileapp

ADD ./tileapp/requirements.txt /tmp/requirements.txt
RUN conda install --file /tmprequirements.txt

ADD ./secret_key.py /tmp/secret_key.py
RUN export SECRET_KEY="python secret_key.py"
ENV TF_VAR_secret_key=$SECRET_KEY
# ENV TF_VAR_secret_key="python secret_key.py"

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
