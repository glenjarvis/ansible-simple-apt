# python-apt-venv

## Use Ansible Apt in a Virtual Env

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

This project is a fork of the Python package **python-apt** so that Ansible can
use the Ansible **apt** module to install on Debian style hosts when the
**interpreter_python** is set to a location other than **/usr/bin/python**.

## Why Use a Virtualenv for Ansible?

The question often comes up, *Why do this?* Isn't it easier to use the
system-level Python? 

It is true that this package was written by Ubuntu developers and is packaged
as a Debian package. And, it was written to be used in Debian packages.

However, since the Ansible **apt** module has been written to use this package,
having it tightly coupled with the system level Python makes it difficult for
some tasks, such as Python3 support in Ansible on older Debian hosts.

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

## Can you work around this?

Actually, there are work-arounds that have been successful. None of them are
ideal or without human error.


### First work-around: Avoid apt module

One can avoid the Ansible **apt** module completely. The shell or command
module could create a new process and use the Apt CLI:

```
- name: Demo Shell Workaround
  hosts: localhost
  tasks:
    - shell: apt-get install -y cowsay
      become: yes
```

Although this works, there are several drawbacks:

* Like most shell/command tasks, this will show the task as **changed** even if the package was already installed.
* These 'apt' tasks may creep back in and have to be maintained by Peer Review (automatic or human)
* There may be a large code base and/or infrastructure in place where such a change is impractical
* A warning will be prompted to prompt uses to run apt-get as shown below

```
TASK [shell] ************************************************************************************************************************************************
[WARNING]: Consider using the apt module rather than running 'apt-get'.  If you need to use command because apt is insufficient you can add 'warn: false' to
this command task or set 'command_warnings=False' in ansible.cfg to get rid of this message.
changed: [localhost]
```


### Second work-around: Write a custom/fork Ansible apt module

One could write a custom Ansible **apt** module (e.g., **apt-new**). 

If the module avoided the imports and used subprocesses to execute commands,
this could work well. This could be used to customize messages and behavior.

However, there are still drawbacks:

* The original **apt** (e.g., instead of **apt-new**) tasks may creep back in and have to be maintained by Peer Review (automatic or human)
* There may be a large code base and/or infrastructure in place where such a change is impractical
* Naming this new module may be hard


## Can't you just install the python-apt package inside of the VirtualEnv?

Actually, no. That's the purpose of this fork/repo - to enable that installation.

When trying to do so, you may see an error similar to:

```
    default:       File "<string>", line 1, in <module>
    default:       File "/tmp/pip-req-build-CVYOcN/setup.py", line 6, in <module>
    default:         from DistUtilsExtra.command import *
    default:     ImportError: No module named DistUtilsExtra.command
```

See the **02_install_problem_demo** subdirectory in this repo for a full
demonstration using **Vagrant**.


## Is this released yet?

Actually, no. **I NEED YOUR HELP**. 

Most of the issues that I see here are simple enough - stale packaging (e.g.,
using Distutils). I've been able to work around most issues. HOWEVER, I'm
having difficulty with the extension compilation (**apt_inst** and
**apt_pkg**).

Ideally, we modernize this enough to use **wheels** so we don't have to compile
on installation. 

**I'm stuck**

**Please help**
