###########
# BUILDER #
###########

# pull official base image
FROM python:3.11 as builder

ENV DEBIAN_FRONTEND noninteractive

# set work directory
WORKDIR /usr/src/CopyCentral_Hub

COPY . /usr/src/CopyCentral_Hub/

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/CopyCentral_Hub/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.11

# create directory for the app user
RUN mkdir -p /home/CopyCentral_Hub

# create the app user
RUN apt-get update && apt-get install -y adduser

RUN addgroup --system copycentralhub && adduser --system --group copycentralhub

# create the appropriate directories
ENV HOME=/home/CopyCentral_Hub
ENV APP_HOME=/home/CopyCentral_Hub/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get install -y libreoffice libreoffice-writer
RUN apt-get install -y libreoffice-java-common
COPY --from=builder /usr/src/CopyCentral_Hub/wheels /wheels
COPY --from=builder /usr/src/CopyCentral_Hub/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint.prod.sh
COPY ./entrypoint.prod.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.prod.sh
RUN chmod +x  $APP_HOME/entrypoint.prod.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R copycentralhub:copycentralhub $APP_HOME

# change to the app user

# run entrypoint.prod.sh
ENTRYPOINT ["/home/CopyCentral_Hub/web/entrypoint.prod.sh"]