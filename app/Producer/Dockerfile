#Fetches the image of python 3.11.4 from the docker hub
FROM python:3.11.4



#The below line makes to excute the further command in the below directory inside the container
WORKDIR /SCMEXPERT/app/Producer

#The below line  copies the contents of the current directory (where the Dockerfile is located) into the proj/producer directory inside the container. 
#This includes all the files and directories present in the same directory as the Dockerfile.
COPY SCMEXPERT/app/Producer .

RUN pip3 install python-dotenv kafka-python


#whenever container runs, this default command will be executed..
CMD ["python", "producer.py"]