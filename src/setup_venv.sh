#!/bin/bash

echo "Setting up Vagrant host"
sudo apt-get update
sudo apt-get install -y virtualenv
sudo apt-get install python-pip-whl

/sbin/runuser -l vagrant -c '/usr/bin/virtualenv /vagrant/venv'
source /vagrant/venv/bin/activate
/vagrant/venv/bin/pip install --upgrade pip
/vagrant/venv/bin/pip install wheel
/vagrant/venv/bin/pip install ansible

cd /vagrant
ansible --version

/vagrant/venv/bin/ansible-playbook demo.yml
