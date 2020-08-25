# Demo 2 Showing Python Package Behavior installing in Venv

## Vagrant

Because this is Debian specific, its easier to see this runthrough with Vagrant.

### Preparatory Steps
1. Ensure VirtualBox is installed for the Debian "Box"
2. Ensure Vagrant is installed (e.g., `brew install vagrant`)

### Demo Steps
1. `cd 02_install_problem_demo`
2. `vagrant up`
3. The error at the bottom is intentional - this is the error we are demonstrating.
```
    default:       File "/tmp/pip-req-build-Z_S7sN/setup.py", line 6, in <module>
    default:         from DistUtilsExtra.command import *
    default:     ImportError: No module named DistUtilsExtra.command
```
4. Don't forget to `vagrant destroy` when you are done (to save computer resources)


## Full output

If you don't want to install Vagrant or VirtualBox, a sample output of this is in `vagrant_up_output.txt`
