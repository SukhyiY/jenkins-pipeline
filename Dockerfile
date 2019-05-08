ROM python:3.6
LABEL author="Yaroslav"
WORKDIR /flask
COPY ./flask-server.py ./flask-server.py
RUN pip install flask
EXPOSE 80
CMD python3 flask-server.py
