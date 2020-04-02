#!/bin/bash
# A shell script to deploy the latest version of Colossus to the PythonAnywhere server.

export project_name = Colossus

echo "Trying to SSH into PythonAnywhere.."
sshpass -p $1 ssh -o StrictHostKeyChecking=no $project_name@ssh.pythonanywhere.com << EOF
    cd ~/$project_name; ~/$project_name/rebuild.sh $2
EOF