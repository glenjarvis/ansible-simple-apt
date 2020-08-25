#!/bin/bash

echo "Setting up Vagrant host"
sudo aptitude update
sudo aptitude install -y virtualenv

/usr/bin/virtualenv /vagrant/venv

source /vagrant/venv/bin/activate
/vagrant/venv/bin/pip install --upgrade pip
/vagrant/venv/bin/pip install wheel
/vagrant/venv/bin/pip install ansible

cd /vagrant
/vagrant/venv/bin/ansible-playbook demo.yml
