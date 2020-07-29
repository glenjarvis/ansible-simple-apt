# ansible-simple-apt
## Simpler Apt module for Ansible

## Objective

To build an Ansible **apt** module that does not depend upon the **python-apt**
(or **python3-apt**) library. This is necessary to fully support Ansible in a
virtualenv (a common usecase when transitioning the Ansible environment from
Python2 to Python3).

## Background

### The Problem

Since 2013, the Ansible **apt** module has depended upon a the **python-apt**
(or **python3-apt**) library. However those libraries are not supported outside
of a Debian packaging environment.

[Debian Bug #845330](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=845330)
> Julian Andres Klode <jak@debian.org>
> Aargh, not this whole PyPI thing again. Nobody ever officially uploaded
> python-apt there. It is tightly coupled with APT, and not supposed to be
> distributed in any fashion other than via Debian packages.There is no, and
> has never been any support for PyPi. And I can say that I have absolutely no
> interest in duplicating work there.

Although there is a Python Package Index (PyPI) for this library, there were
only two releases (2012, and 2015) with dubious semantic versioning. They also
do not install in a virtualenv.

### Why do we use the **python-apt** in the Ansible **apt** module?

There was an Ansible bug reported:
https://github.com/ansible/ansible/issues/3421

And, in September 2013, a fix went into place

>    Use low-level package objects in the apt module to check installed state
>
>    Packages which are half-installed are not adequately represented by
>    the .is_installed field of the apt.package.Package object. By using the
>    lower-level apt_pkg.Package object (which provides the .current_state
>    field), we can check for a partially-installed state more accurately.
>
>    Fixes #3421

However, it is still unclear why this was necessary since:

* `dpkg -l` shows state and version.  state 'ii' is "fully installed, for realz"
* `dpkg -L` shows files included in package.

The command line is already being used in other parts of this module. So, we
wish to fall-back to only that implementation. Although we hope to keep all
functionality in the current Ansible **apt** module, we are willing to
sacrifice some behavior for the simplicity of the implementation. It is still
not known if any behavior will be lost.

### Icing on the cake

If the Ansible **apt** package does not find the **python-apt** (or
**python3-apt**) installed, it immediately tries to install it for you -
without prompting or asking.

The original author of this apt fork would prefer to choose the packages to
install, or at least have to confirm them instead of having them
"auto-magically" install themselves.


## Example Use Case

The motivation for the author to create this fork of Ansible apt was to support
Ansible running completely in a Python virutal environment. (e.g., when the
**interpreter_python** is set to a location other than **/usr/bin/python**.)

### Why Use a Virtualenv for Ansible?

The question often comes up, *Why do this?* Isn't it easier to use the
system-level Python?

The original author of this fork had to help manage a transition for Ansible,
running in Python3 on over 8,000 hosts -- all of them already in production
with a system Python of Python2.

There really is no other way to keep this tame except to have a controlled
python virtual environment for Ansible and to explicitly set the
**interpreter_python**


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

