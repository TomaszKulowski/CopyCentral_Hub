###########
# BUILDER #
###########

# pull official base image
FROM python:3.11 as builder

ENV DEBIAN_FRONTEND noninteractive

# set work directory
WORKDIR /usr/src/CopyCentral_Hub

COPY . /usr/src/CopyCentral_Hub/

RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get install -y gdal-bin libgdal-dev build-essential


# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/CopyCentral_Hub/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.11

# create directory for the copycentralhub user
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
RUN apt-get install -y libreoffice-writer gettext
RUN apt-get install -y libreoffice-java-common
RUN apt-get install -y gdal-bin libgdal-dev build-essential

ENV GDAL_LIBRARY_PATH /usr/lib/libgdal.so

COPY --from=builder /usr/src/CopyCentral_Hub/wheels /wheels
COPY --from=builder /usr/src/CopyCentral_Hub/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# install redis
RUN apt-get install -y redis-server

# expose Redis port
EXPOSE 6379

COPY ./entrypoint.prod.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.prod.sh
RUN chmod +x  $APP_HOME/entrypoint.prod.sh

# copy project
COPY . $APP_HOME

# chown all the files to the copycentralhub user
RUN chown -R copycentralhub:copycentralhub $HOME
RUN chmod +x  $APP_HOME/entrypoint.prod.sh


# change to the copycentralhub user
USER copycentralhub

# run entrypoint.prod.sh
ENTRYPOINT ["/home/CopyCentral_Hub/web/entrypoint.prod.sh"]