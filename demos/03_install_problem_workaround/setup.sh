#!/bin/bash

set -e

echo "Setting up Vagrant host"
sudo aptitude update
sudo aptitude install -y virtualenv
sudo aptitude install -y git
sudo aptitude install -y python-dev
sudo aptitude install -y libapt-pkg-dev
sudo aptitude install -y build-essential
sudo aptitude install -y intltool  # Not optional after all

/usr/bin/virtualenv /vagrant/venv
source /vagrant/venv/bin/activate
/vagrant/venv/bin/pip install --upgrade pip
/vagrant/venv/bin/pip install wheel

cd /vagrant
/vagrant/venv/bin/pip install git+https://salsa.debian.org/python-debian-team/python-debian
/vagrant/venv/bin/pip install git+https://salsa.debian.org/python-team/modules/python-distutils-extra
/vagrant/venv/bin/pip install git+https://salsa.debian.org/apt-team/python-apt@debian/jessie --no-clean  # To keep created wheel
