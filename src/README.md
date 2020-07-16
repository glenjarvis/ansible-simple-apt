FORK HISTORY
============

In an effort to ensure we understand that any changes that we make will still
work with previous versions of Ansible, the apt.py module (and it's previous
name of apt) was copied from different versions of Ansible so we could have one
place to compare changes being made.

Each of these Ansible apt packages were also tested with 'debian/jessie64'
Vagrant box:

history/2.9.10
history/2.8.13
history/2.7.18
history/2.6.20
history/2.5.15
history/2.4.6.0
history/2.4.5.0
history/2.4.4.0
history/2.4.3.0
history/2.4.2.0
history/2.4.1.0
history/2.4.0.0

Note that previous versions to 2.4.0.0 will not install Ansible in this demo
setup on debian/jessie64 because the pycrypto dependency does not install.


However, when browing historical source, we see the initial apt module was
created (without this python-apt) dependency -- command line only on 
Mon Mar 26 12:49:13 2012

The problematic dependency for the the `python-apt` library was added on Sep 11.
It was added to fix this bug:
https://github.com/ansible/ansible/issues/3421

Although Ansible version releases started at 1.0.0, the following directories
were used for consistency:

history/0.0.0.0: Initial version (no library) / 2012-03-26 
history/0.0.0.1: First intro of now-problematic library dependency / 2013-09-11

