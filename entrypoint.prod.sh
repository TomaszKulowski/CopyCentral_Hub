#!/bin/sh

# Check if the database is PostgreSQL and wait for it to be ready
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for PostgreSQL..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Perform Django initialization tasks if the initialization file does not exist
if [ ! -f /home/CopyCentral_Hub/web/.initialized ]; then
    echo "Running Django initialization..."

    # Make migrations
    python manage.py makemigrations

    # Apply migrations
    python manage.py migrate

    # Generate translation files
    python manage.py makemessages -l pl

    # Compile translation files
    python manage.py compilemessages

    # Ensure permissions for staticfiles
    chown -R copycentralhub:copycentralhub /home/CopyCentral_Hub/web/staticfiles

    # Collect static files
    python manage.py collectstatic --noinput

    # Create a file to signal initialization is complete
    touch /home/CopyCentral_Hub/web/.initialized

    echo "Django initialization complete"
else
    echo "Django initialization has already been done."
fi

# Execute the command passed to the container
exec "$@"
