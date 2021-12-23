FROM python:3.7.3-alpine3.9 as prod
RUN mkdir /app/
WORKDIR /app/
COPY . /app
RUN pip install -r requirements.txt
ENV MY_USER root
ENV MY_PASS root
ENV MY_HOST db
ENV MY_PORT 3306
ENV MY_DB custmet
ENTRYPOINT ["python"]
CMD [ "app.py" ]
