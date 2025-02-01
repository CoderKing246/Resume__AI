#!/bin/bash

# Exit on error
set -e

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install spaCy model manually if not already present
echo "Installing spaCy model..."
python -m spacy download en-core-web-sm

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Run any additional custom build commands (if any)
# For example, creating a database or setting up other services

echo "Build complete!"
