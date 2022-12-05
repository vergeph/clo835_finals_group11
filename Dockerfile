FROM ubuntu:20.04
RUN apt-get update -y
COPY . /app
WORKDIR /app
RUN set -xe \
    && apt-get update -y \
    && apt-get install vim -y \
    && apt-get install -y python3-pip \
    && apt-get install -y mysql-client 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#RUN aws s3 cp s3://clo835-finals-group11/back1.jpeg back1.jpeg \
    #&& aws s3 cp s3://clo835-finals-group11/back2.jpeg back2.jpeg \
    #&& aws s3 cp s3://clo835-finals-group11/back3.jpeg back3.jpeg
EXPOSE 81
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]