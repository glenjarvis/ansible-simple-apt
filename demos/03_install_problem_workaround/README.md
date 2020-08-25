# Demo 3 Demonstrating a Work around from Stefan Taranu

In trying to solve this, I took a stab at posting this repo on Upwork to see
who could help me. Although most couldn't, I found Stefan Taranu
(https://www.upwork.com/fl/stefantaranu) who was able to find this work-around.
He was great! I recommend him.

See also this bug report from Debian:
https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=845330

## Vagrant

Because this is Debian specific, its easier to see this runthrough with Vagrant.

### Preparatory Steps
1. Ensure VirtualBox is installed
2. Ensure Vagrant is installed (e.g., `brew install vagrant`)

### Demo Steps
1. `cd 03_install_problem_workaround`
2. `vagrant up`
3. Notice that this installs now.
4. cd /vagrant
5. /vagrant/venv/bin/ansible-playbook demo.yml
6. Don't forget to `vagrant destroy` when you are done (to save computer resources)

## Full output

If you don't want to install Vagrant or VirtualBox, a sample output of this is in `vagrant_up_output.txt`

## Bonus

The python_apt wheel was preserved with the --no-clean argument added to the pip install. Notice from the vagrant_up_output.txt example:

    default:   Created wheel for python-apt: filename=python_apt-0.0.0-cp27-cp27mu-linux_x86_64.whl size=1267219 sha256=ecda5001a009bd08f42967d2a61abcc02895685968a7bf716487a1d5dddb6c63
    default:   Stored in directory: /tmp/pip-ephem-wheel-cache-RmrwF8/wheels/be/ba/c7/4ded2b16afd7125934d6b7a9e6086e71da2d35442e6bf450ac

You can fetch this weel (e.g., python_apt-0.0.0-cp27-cp27mu-linux_x86_64.whl) to save having to compile for similar hardware/OS.
