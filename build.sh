#!/bin/bash

# Exit on error
set -e

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install spaCy model
echo "Installing spaCy model..."
python -m spacy download en-core-web-sm

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create a superuser if one doesn't exist (optional)
# python manage.py createsuperuser --noinput

# Run any additional custom build commands (if any)
# For example, creating a database or setting up other services

# If you're using AWS for storage or any additional configuration, handle it here.
# aws s3 cp my_file s3://my_bucket --region us-west-2

echo "Build complete!"
