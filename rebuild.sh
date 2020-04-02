#!/bin/bash
# Script to automate pulling of project updates, installation of
# dependencies and reloading the application in production

echo "Fetching updates from the Git Repository.."
git pull origin master
# Activate virtual environment:
source /home/colossus/.virtualenvs/colossus/bin/activate
# Install requirements:
pip install -r requirements/production.txt
echo "Now, rebooting the server.."
API_TOKEN=$1 pa_reload_webapp.py colossus.pythonanywhere.com
touch reboot
