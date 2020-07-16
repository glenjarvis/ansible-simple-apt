# ansible-simple-apt

# Objective

Remove the library dependency that blocks Ansible's use of apt in a
Virtual env.

```
if sys.version_info[0] < 3:
    PYTHON_APT = 'python-apt'
else:
    PYTHON_APT = 'python3-apt'
```

Keep the same functionality without using this library. The command line is
already being used, can the same behavior also be achieved without the library.

Root cause for adding the library was to fix this issue in 2013:

https://github.com/ansible/ansible/issues/3421



# Why

## Use Simpler Apt for Ansible in a Virtual Env

By default, the [Ansible apt
module](https://docs.ansible.com/ansible/latest/modules/apt_module.html)
requires the **apt**, **apt.debfile**, and **apt_pkg** packages to import:

```HAS_PYTHON_APT = True
try:
    import apt
    import apt.debfile
    import apt_pkg
except ImportError:
    HAS_PYTHON_APT = False

if sys.version_info[0] < 3:
    PYTHON_APT = 'python-apt'
else:
    PYTHON_APT = 'python3-apt'
```
    
This comes from the **python-apt** package. However, those packages do not
install in a Python virtualenv (2 nor 3). They were originally created to be
installed in the sytem-level Python.

The **python-apt** package isn't actually necessary (the Ansible apt module
uses the command line to do the apt install).

This project is a fork of the Ansible **apt** module so that Ansible can be
used from a Virtual Environment (e.g., when the **interpreter_python** is set
to a location other than **/usr/bin/python**.)

## Why Use a Virtualenv for Ansible?

The question often comes up, *Why do this?* Isn't it easier to use the
system-level Python? 

It is true that the **python-apt** or **python3-apt** package was written by
Ubuntu developers and is packaged as a Debian package. And, it was written to
be used in Debian packages.

However, since the Ansible **apt** module has been written to use the
**python-apt** packages, having it tightly coupled with the system level Python
makes it difficult for some tasks, such as Python3 support in Ansible on older
Debian hosts.


## What symptoms do you see in the venv / apt scenario?

The task will fail with the message **Could not import python modules: apt,
apt_pkg. Please install python-apt package.**.

```
    default: PLAY [Demo Playbook] ***********************************************************
    default:
    default: TASK [Gathering Facts] *********************************************************
    default: ok: [localhost]
    default:
    default: TASK [apt] *********************************************************************
    default: [WARNING]: Updating cache and auto-installing missing dependency: python-apt
    default: fatal: [localhost]: FAILED! => {"changed": false, "msg": "Could not import python modules: apt, apt_pkg. Please install python-apt package."}
    default:
    default: PLAY RECAP *********************************************************************
    default: localhost                  : ok=3    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
```

See the **01_ansible_venv_problem_demo** subdirectory in this repo for a full
demonstration using **Vagrant**.

