#!/bin/bash

echo "Setting up Vagrant host"
sudo aptitude update
sudo aptitude install -y virtualenv

/usr/bin/virtualenv /vagrant/venv
source /vagrant/venv/bin/activate
/vagrant/venv/bin/pip install --upgrade pip
/vagrant/venv/bin/pip install wheel

echo "Next steps:"
echo "  vagrant ssh"
echo "sudo su -"
echo "cd /vagrant/python-apt-venv/"
echo "/vagrant/venv/bin/pip install ."
