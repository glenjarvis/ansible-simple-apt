#!/bin/bash

echo "Setting up for Demo 01"
sudo /usr/bin/apt update
sudo apt-get install -y python3-venv
sudo apt-get install -y ansible  # Intentionally creating two different Ansible locations

echo "Building Virtualenv"
cd /vagrant
/usr/bin/python3 -m venv tools_venv
/vagrant/tools_venv/bin/pip install --upgrade pip
/vagrant/tools_venv/bin/pip install wheel
/vagrant/tools_venv/bin/pip install ansible

/usr/bin/python3 -m venv venv
source /vagrant/venv/bin/activate

/vagrant/venv/bin/pip install --upgrade pip
/vagrant/venv/bin/pip install wheel
/vagrant/venv/bin/pip install ansible

/vagrant/venv/bin/ansible-playbook -v demo.yml

echo "Notice which Python is being used..."
ANSIBLE_DEBUG=1 /vagrant/venv/bin/ansible-playbook demo.yml | grep _low_level_execute_command | grep python

echo "Breaking peripheral virtualenv..."
mv /vagrant/tools_venv /vagrant/tools_venv_broken

echo "Running again..."
/vagrant/venv/bin/ansible-playbook -v demo.yml
