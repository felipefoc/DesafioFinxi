# base image  
FROM python:3.9-alpine3.13  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1  
# install dependencies  
RUN pip install --upgrade pip  

RUN mkdir /app
# copy whole project to your docker home directory. 
COPY . /app

WORKDIR /app
# run this command to install all dependencies  
RUN pip install -r requirements.txt  
# port where the Django app runs  
EXPOSE 8000  

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]

