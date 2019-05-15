FROM python:3.6
LABEL author="Yaroslav"
WORKDIR /flask
COPY ./webapp.py ./webapp.py
RUN pip install flask
EXPOSE 80
CMD python3 webapp.py
