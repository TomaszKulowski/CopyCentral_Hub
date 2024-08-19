###########
# BUILDER #
###########

# Use the official Python image as a base for the build stage
FROM python:3.11 as builder

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/CopyCentral_Hub

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Install Python dependencies into wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/CopyCentral_Hub/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.11

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    HOME=/home/CopyCentral_Hub \
    APP_HOME=/home/CopyCentral_Hub/web \
    GDAL_LIBRARY_PATH=/usr/lib/libgdal.so \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create directories and set work directory
RUN mkdir -p $APP_HOME/staticfiles $APP_HOME/mediafiles
WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    libreoffice-writer \
    gettext \
    libreoffice-java-common \
    gdal-bin \
    libgdal-dev \
    build-essential \
    redis-server \
    adduser \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a system user and group
RUN addgroup --system copycentralhub && adduser --system --ingroup copycentralhub copycentralhub

# Install Python dependencies
COPY --from=builder /usr/src/CopyCentral_Hub/wheels /wheels
COPY --from=builder /usr/src/CopyCentral_Hub/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application scripts and grant execution permissions
COPY entrypoint.prod.sh .
RUN chmod +x entrypoint.prod.sh && sed -i 's/\r$//g' entrypoint.prod.sh

# Copy the application code
COPY . .

# Adjust file ownership and permissions
RUN chown -R copycentralhub:copycentralhub $HOME $APP_HOME/staticfiles $APP_HOME/mediafiles $APP_HOME/locale

# Expose Redis port
EXPOSE 6379

# Switch to non-root user
USER copycentralhub

# Set the entry point for the container
ENTRYPOINT ["./entrypoint.prod.sh"]
