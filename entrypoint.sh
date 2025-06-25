#!/bin/bash

# Ensure log file exists and has correct permissions
touch /app/django-error.log
chmod 666 /app/django-error.log
chown appuser:appuser /app/django-error.log

# Ensure the staticfiles directory has correct permissions
mkdir -p /app/staticfiles
chmod 777 /app/staticfiles
chown appuser:appuser /app/staticfiles

# Switch to the appuser
exec gosu appuser "$@"
