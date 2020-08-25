# Demo 1 Showing Ansible Behavior in Venv

## Vagrant

Because this is Debian specific, its easier to see this runthrough with Vagrant.

### Preparatory Steps
1. Ensure VirtualBox is installed for the Debian "Box"
2. Ensure Vagrant is installed (e.g., `brew install vagrant`)

### Demo Steps
1. Change to this directory
2. `vagrant up`

TODO: Add notes regarding:
a. Debugging version used: _low_level_execute_command(): executing: /bin/sh -c '/vagrant/venv/bin/python3 /root/ 
b. Rewriting of Ansible (e.g., modules/fizz.py is rewritten correctly:  #!/vagrant/tools_venv/bin/python) 
c. How these rewritings are NOT rewritten: (my_random_tool.py #!/vagrant/tools_venv/bin/python)
d. Consequence of the above: /bin/sh: 1: /root/.ansible/tmp/ansible-tmp-1598331391.7026846-3010-173242588552017/my_random_tool.py: not found

## Full output

If you don't want to install Vagrant or VirtualBox, a sample output of this is in `vagrant_up_output.txt`
