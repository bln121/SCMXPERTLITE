#Fetches the image of python 3.11.4 from the docker hub
FROM python:3.11.4



#This line sets the working directory inside the container to /SCMEXPERT/app/Consumer. Any subsequent commands or instructions will be executed in this directory within the container.
WORKDIR /SCMXPERT/app

#This line copies the contents of the current directory into the above mentioned container's workdir
COPY . .


#This line runs the pip3 install command inside the container to install the specified Python packages.
RUN apt-get update && apt-get install -y python3-pip && pip3 install -r requirements.txt

#whenever container runs, this default command will be executed..
#CMD [ "python", "main:app"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]