FROM python:3

WORKDIR /usr/src/app

#Copy the content of the current folder in /usr/src/app
#ignoring the files specified in the .dockerignore file
COPY . .

#Program to be run
RUN pip3 install -r requirements.txt

#First command to be executed when the container runs
CMD ["python3", "./telephone.py"]

#Port to exposed in the container
#EXPOSE 8080