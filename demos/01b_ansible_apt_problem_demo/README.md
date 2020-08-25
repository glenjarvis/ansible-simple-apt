# Demo 1 Showing Ansible Behavior in Venv with Apt

## Vagrant

Because this is Debian specific, its easier to see this runthrough with Vagrant.

### Preparatory Steps
1. Ensure VirtualBox is installed for the Debian "Box"
2. Ensure Vagrant is installed (e.g., `brew install vagrant`)

### Demo Steps
1. `cd 01_ansible_venv_problem_demo`
2. `vagrant up`
3. The error at the bottom is intentional - this is the error we are demonstrating.
```
    default: TASK [apt] *********************************************************************
    default: [WARNING]: Updating cache and auto-installing missing dependency: python-apt
    default: fatal: [localhost]: FAILED! => {"changed": false, "msg": "Could not import python modules: apt, apt_pkg. Please install python-apt package."}
    default:
```
4. Don't forget to `vagrant destroy` when you are done (to save computer resources)


## Full output

If you don't want to install Vagrant or VirtualBox, a sample output of this is in `vagrant_up_output.txt`
