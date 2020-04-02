#!/bin/bash
# Script to automate pulling of project updates, installation of
# dependencies and reloading the application in production

# Pull updates from Git repository
git pull origin master
# Activate virtual environment:
source /home/colossus/.virtualenvs/colossus/bin/activate
# Install requirements:
pip install -r requirements/production.txt
# Reloading the application
API_TOKEN=$1 pa_reload_webapp.py colossus.pythonanywhere.com
touch reboot
