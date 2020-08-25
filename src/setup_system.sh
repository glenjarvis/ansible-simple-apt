#!/bin/bash

# Install python_apt on system level
#
# This setup uses the root file system for setup. This is needed if we want to
# install and gather debugging information on the python_apt library. We then
# recrod that debugging information, destroy the vagrant box, and rebuild using
# setup_venv.sh (instead of this file).

echo "Setting up Vagrant host"
sudo apt-get install -y python-pip-whl
sudo apt-get install -y python-pip
sudo pip install --upgrade pip
sudo pip install ansible  # Note this is often a lower version (like 1.7.2) vs
                          # later versions (like 2.9.10)

cd /vagrant
ansible --version

ansible-playbook demo.yml
