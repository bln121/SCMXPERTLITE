#Fetches the image of python 3.11.4 from the docker hub
FROM python:3.11.4



#This line sets the working directory inside the container to /SCMEXPERT/app/Socket_connection. Any subsequent commands or instructions will be executed in this directory within the container.
WORKDIR /SCMXPERT/app/Socket_connection

#This line copies the contents of the current directory into the above mentioned container's workdir
COPY . .


#This line runs the pip3 install command inside the container to install the specified Python packages.
RUN pip3 install python-dotenv kafka-python

EXPOSE 23532

#whenever container runs, this default command will be executed..
CMD ["python", "server.py"]