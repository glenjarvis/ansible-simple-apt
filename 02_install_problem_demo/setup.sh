#!/bin/bash

echo "Setting up Vagrant host"
sudo aptitude update
sudo aptitude install -y virtualenv

/usr/bin/virtualenv /vagrant/venv
source /vagrant/venv/bin/activate
/vagrant/venv/bin/pip install --upgrade pip
/vagrant/venv/bin/pip install wheel

cd /vagrant
tar -xvf python-apt-0.7.8.tar.bz2
cd /vagrant/python-apt-0.7.8
/vagrant/venv/bin/pip install .
