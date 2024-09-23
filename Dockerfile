FROM python:3.6

# root directory for our project in the container
RUN mkdir /auth-service

# working directory
WORKDIR /auth-service

# copy requirements.txt file
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

# copy the current directory contents into the container
ADD . /auth-service/

# run `./runserver.sh` command
CMD ["./runserver.sh"]