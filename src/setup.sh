#!/bin/bash

echo "Setting up Vagrant host"
sudo aptitude update
sudo aptitude install -y virtualenv

/sbin/runuser -l vagrant -c '/usr/bin/virtualenv /vagrant/venv'
/vagrant/venv/bin/activate
/vagrant/venv/bin/pip install --upgrade pip
/vagrant/venv/bin/pip install wheel
/vagrant/venv/bin/pip install ansible

cd /vagrant
ansible --version

/vagrant/venv/bin/ansible-playbook demo.yml
