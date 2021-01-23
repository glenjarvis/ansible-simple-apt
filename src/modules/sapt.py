#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2012, Flowroute LLC
# Written by Matthew Williams <matthew@flowroute.com>
# Based on yum module written by Seth Vidal <skvidal at fedoraproject.org>

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: apt
short_description: Manages apt-packages
description:
  - Manages I(apt) packages (such as for Debian/Ubuntu).
version_added: "0.0.2"
options:
  name:
    description:
      - A list of package names, like C(foo), or package specifier with version, like C(foo=1.0).
        Name wildcards (fnmatch) like C(apt*) and version wildcards like C(foo=1.0*) are also supported.
    aliases: [ package, pkg ]
  state:
    description:
      - Indicates the desired package state. C(latest) ensures that the latest version is installed. C(build-dep) ensures the package build dependencies
        are installed. C(fixed) attempt to correct a system with broken dependencies in place.
    default: present
    choices: [ absent, build-dep, latest, present, fixed ]
  update_cache:
    description:
      - Run the equivalent of C(apt-get update) before the operation. Can be run as part of the package installation or as a separate step.
    type: bool
    default: 'no'
  cache_valid_time:
    description:
      - Update the apt cache if its older than the I(cache_valid_time). This option is set in seconds.
      - As of Ansible 2.4, if explicitly set, this sets I(update_cache=yes).
    default: 0
  purge:
    description:
     - Will force purging of configuration files if the module state is set to I(absent).
    type: bool
    default: 'no'
  default_release:
    description:
      - Corresponds to the C(-t) option for I(apt) and sets pin priorities
  install_recommends:
    description:
      - Corresponds to the C(--no-install-recommends) option for I(apt). C(yes) installs recommended packages.  C(no) does not install
        recommended packages. By default, Ansible will use the same defaults as the operating system. Suggested packages are never installed.
    aliases: ['install-recommends']
    type: bool
  force:
    description:
      - 'Corresponds to the C(--force-yes) to I(apt-get) and implies C(allow_unauthenticated: yes)'
      - "This option will disable checking both the packages' signatures and the certificates of the
        web servers they are downloaded from."
      - 'This option *is not* the equivalent of passing the C(-f) flag to I(apt-get) on the command line'
      - '**This is a destructive operation with the potential to destroy your system, and it should almost never be used.**
         Please also see C(man apt-get) for more information.'
    type: bool
    default: 'no'
  allow_unauthenticated:
    description:
      - Ignore if packages cannot be authenticated. This is useful for bootstrapping environments that manage their own apt-key setup.
      - 'C(allow_unauthenticated) is only supported with state: I(install)/I(present)'
    type: bool
    default: 'no'
    version_added: "2.1"
  upgrade:
    description:
      - If yes or safe, performs an aptitude safe-upgrade.
      - If full, performs an aptitude full-upgrade.
      - If dist, performs an apt-get dist-upgrade.
      - 'Note: This does not upgrade a specific package, use state=latest for that.'
      - 'Note: Since 2.4, apt-get is used as a fall-back if aptitude is not present.'
    version_added: "1.1"
    choices: [ dist, full, 'no', safe, 'yes' ]
    default: 'no'
  dpkg_options:
    description:
      - Add dpkg options to apt command. Defaults to '-o "Dpkg::Options::=--force-confdef" -o "Dpkg::Options::=--force-confold"'
      - Options should be supplied as comma separated list
    default: force-confdef,force-confold
  deb:
     description:
       - Path to a .deb package on the remote machine.
       - If :// in the path, ansible will attempt to download deb before installing. (Version added 2.1)
       - Requires the C(xz-utils) package to extract the control file of the deb package to install.
     required: false
     version_added: "1.6"
  autoremove:
    description:
      - If C(yes), remove unused dependency packages for all module states except I(build-dep). It can also be used as the only option.
      - Previous to version 2.4, autoclean was also an alias for autoremove, now it is its own separate command. See documentation for further information.
    type: bool
    default: 'no'
    version_added: "2.1"
  autoclean:
    description:
      - If C(yes), cleans the local repository of retrieved package files that can no longer be downloaded.
    type: bool
    default: 'no'
    version_added: "2.4"
  policy_rc_d:
    description:
      - Force the exit code of /usr/sbin/policy-rc.d.
      - For example, if I(policy_rc_d=101) the installed package will not trigger a service start.
      - If /usr/sbin/policy-rc.d already exist, it is backed up and restored after the package installation.
      - If C(null), the /usr/sbin/policy-rc.d isn't created/changed.
    type: int
    default: null
    version_added: "2.8"
  only_upgrade:
    description:
      - Only upgrade a package if it is already installed.
    type: bool
    default: 'no'
    version_added: "2.1"
  force_apt_get:
    description:
      - Force usage of apt-get instead of aptitude
    type: bool
    default: 'no'
    version_added: "2.4"
requirements:
   - python-apt (python 2)
   - python3-apt (python 3)
   - aptitude (before 2.4)
author: "Matthew Williams (@mgwilliams)"
notes:
   - Three of the upgrade modes (C(full), C(safe) and its alias C(yes)) required C(aptitude) up to 2.3, since 2.4 C(apt-get) is used as a fall-back.
   - In most cases, packages installed with apt will start newly installed services by default. Most distributions have mechanisms to avoid this.
     For example when installing Postgresql-9.5 in Debian 9, creating an excutable shell script (/usr/sbin/policy-rc.d) that throws
     a return code of 101 will stop Postgresql 9.5 starting up after install. Remove the file or remove its execute permission afterwards.
   - The apt-get commandline supports implicit regex matches here but we do not because it can let typos through easier
     (If you typo C(foo) as C(fo) apt-get would install packages that have "fo" in their name with a warning and a prompt for the user.
     Since we don't have warnings and prompts before installing we disallow this.Use an explicit fnmatch pattern if you want wildcarding)
   - When used with a `loop:` each package will be processed individually, it is much more efficient to pass the list directly to the `name` option.
'''

EXAMPLES = '''
- name: Install apache httpd  (state=present is optional)
  apt:
    name: apache2
    state: present

- name: Update repositories cache and install "foo" package
  apt:
    name: foo
    update_cache: yes

- name: Remove "foo" package
  apt:
    name: foo
    state: absent

- name: Install the package "foo"
  apt:
    name: foo

- name: Install a list of packages
  apt:
    pkg:
    - foo
    - foo-tools

- name: Install the version '1.00' of package "foo"
  apt:
    name: foo=1.00

- name: Update the repository cache and update package "nginx" to latest version using default release squeeze-backport
  apt:
    name: nginx
    state: latest
    default_release: squeeze-backports
    update_cache: yes

- name: Install latest version of "openjdk-6-jdk" ignoring "install-recommends"
  apt:
    name: openjdk-6-jdk
    state: latest
    install_recommends: no

- name: Upgrade all packages to the latest version
  apt:
    name: "*"
    state: latest

- name: Update all packages to the latest version
  apt:
    upgrade: dist

- name: Run the equivalent of "apt-get update" as a separate step
  apt:
    update_cache: yes

- name: Only run "update_cache=yes" if the last one is more than 3600 seconds ago
  apt:
    update_cache: yes
    cache_valid_time: 3600

- name: Pass options to dpkg on run
  apt:
    upgrade: dist
    update_cache: yes
    dpkg_options: 'force-confold,force-confdef'

- name: Install a .deb package
  apt:
    deb: /tmp/mypackage.deb

- name: Install the build dependencies for package "foo"
  apt:
    pkg: foo
    state: build-dep

- name: Install a .deb package from the internet.
  apt:
    deb: https://example.com/python-ppq_0.1-1_all.deb

- name: Remove useless packages from the cache
  apt:
    autoclean: yes

- name: Remove dependencies that are no longer required
  apt:
    autoremove: yes

'''

RETURN = '''
cache_updated:
    description: if the cache was updated or not
    returned: success, in some cases
    type: bool
    sample: True
cache_update_time:
    description: time of the last cache update (0 if unknown)
    returned: success, in some cases
    type: int
    sample: 1425828348000
stdout:
    description: output from apt
    returned: success, when needed
    type: str
    sample: "Reading package lists...\nBuilding dependency tree...\nReading state information...\nThe following extra packages will be installed:\n  apache2-bin ..."
stderr:
    description: error output from apt
    returned: success, when needed
    type: str
    sample: "AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.1.1. Set the 'ServerName' directive globally to ..."
'''  # NOQA

# added to stave off future warnings about apt api
import warnings
warnings.filterwarnings('ignore', "apt API not stable yet", FutureWarning)

import datetime
import fnmatch
import itertools
import json
import os
import shutil
import re
import sys
import tempfile
import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes, to_native
from ansible.module_utils.urls import fetch_file

# APT related constants
APT_ENV_VARS = dict(
    DEBIAN_FRONTEND='noninteractive',
    DEBIAN_PRIORITY='critical',
    # We screenscrape apt-get and aptitude output for information so we need
    # to make sure we use the C locale when running commands
    LANG='C',
    LC_ALL='C',
    LC_MESSAGES='C',
    LC_CTYPE='C',
)

DPKG_OPTIONS = 'force-confdef,force-confold'
APT_GET_ZERO = "\n0 upgraded, 0 newly installed"
APTITUDE_ZERO = "\n0 packages upgraded, 0 newly installed"
APT_LISTS_PATH = "/var/lib/apt/lists"
APT_UPDATE_SUCCESS_STAMP_PATH = "/var/lib/apt/periodic/update-success-stamp"
APT_MARK_INVALID_OP = 'Invalid operation'
APT_MARK_INVALID_OP_DEB6 = 'Usage: apt-mark [options] {markauto|unmarkauto} packages'

CLEAN_OP_CHANGED_STR = dict(
    autoremove='The following packages will be REMOVED',
    # "Del python3-q 2.4-1 [24 kB]"
    autoclean='Del ',
)


# TODO: Remove when dependencies are complete
import apt
import apt.debfile
import apt_pkg

if sys.version_info[0] < 3:
    PYTHON_APT = 'python-apt'
else:
    PYTHON_APT = 'python3-apt'


class PolicyRcD(object):
    """
    This class is a context manager for the /usr/sbin/policy-rc.d file.
    It allow the user to prevent dpkg to start the corresponding service when installing
    a package.
    https://people.debian.org/~hmh/invokerc.d-policyrc.d-specification.txt
    """

    def __init__(self, module):
        # we need the module for later use (eg. fail_json)
        self.m = module

        # if policy_rc_d is null then we don't need to modify policy-rc.d
        if self.m.params['policy_rc_d'] is None:
            return

        # if the /usr/sbin/policy-rc.d already exist
        # we will back it up during package installation
        # then restore it
        if os.path.exists('/usr/sbin/policy-rc.d'):
            self.backup_dir = tempfile.mkdtemp(prefix="ansible")
        else:
            self.backup_dir = None

    def __enter__(self):
        """
        This method will be call when we enter the context, before we call `apt-get …`
        """

        # if policy_rc_d is null then we don't need to modify policy-rc.d
        if self.m.params['policy_rc_d'] is None:
            return

        # if the /usr/sbin/policy-rc.d already exist we back it up
        if self.backup_dir:
            try:
                shutil.move('/usr/sbin/policy-rc.d', self.backup_dir)
            except Exception:
                self.m.fail_json(msg="Fail to move /usr/sbin/policy-rc.d to %s" % self.backup_dir)

        # we write /usr/sbin/policy-rc.d so it always exit with code policy_rc_d
        try:
            with open('/usr/sbin/policy-rc.d', 'w') as policy_rc_d:
                policy_rc_d.write('#!/bin/sh\nexit %d\n' % self.m.params['policy_rc_d'])

            os.chmod('/usr/sbin/policy-rc.d', 0o0755)
        except Exception:
            self.m.fail_json(msg="Failed to create or chmod /usr/sbin/policy-rc.d")

    def __exit__(self, type, value, traceback):
        """
        This method will be call when we enter the context, before we call `apt-get …`
        """

        # if policy_rc_d is null then we don't need to modify policy-rc.d
        if self.m.params['policy_rc_d'] is None:
            return

        if self.backup_dir:
            # if /usr/sbin/policy-rc.d already exists before the call to __enter__
            # we restore it (from the backup done in __enter__)
            try:
                shutil.move(os.path.join(self.backup_dir, 'policy-rc.d'),
                            '/usr/sbin/policy-rc.d')
                os.rmdir(self.tmpdir_name)
            except Exception:
                self.m.fail_json(msg="Fail to move back %s to /usr/sbin/policy-rc.d"
                                     % os.path.join(self.backup_dir, 'policy-rc.d'))
        else:
            # if they wheren't any /usr/sbin/policy-rc.d file before the call to __enter__
            # we just remove the file
            try:
                os.remove('/usr/sbin/policy-rc.d')
            except Exception:
                self.m.fail_json(msg="Fail to remove /usr/sbin/policy-rc.d (after package manipulation)")


def package_split(pkgspec):
    parts = pkgspec.split('=', 1)
    version = None
    if len(parts) > 1:
        version = parts[1]
    return parts[0], version


def package_versions(pkgname, pkg, pkg_cache):
    try:
        versions = set(p.version for p in pkg.versions)
    except AttributeError:
        # assume older version of python-apt is installed
        # apt.package.Package#versions require python-apt >= 0.7.9.
        pkg_cache_list = (p for p in pkg_cache.Packages if p.Name == pkgname)
        pkg_versions = (p.VersionList for p in pkg_cache_list)
        versions = set(p.VerStr for p in itertools.chain(*pkg_versions))

    return versions


def package_version_compare(version, other_version):
    try:
        return apt_pkg.version_compare(version, other_version)
    except AttributeError:
        return apt_pkg.VersionCompare(version, other_version)

###########################################
# BEGIN package_status (python_apt removal)
###########################################
# This fork was created to remove the dependencies on the python_apt library.
# Until the library is completely removed, each changes are being completely
# contained within this BEGIN/END block of code.
#
# After the library is completely removed and we have an adequate set of tests,
# then, we can begin to refactor and clean this so that it is more organized
# and manageable.

def _count_leading_spaces(line):
    """Given a single line, return how many spaces are in front

    Args:
        line -- single line (typically from command line output)

    Returns:
        Number of spaces (int) preceeding the first non-space character
    """
    count = 0
    for character in line:
        count += 1
        if character != " ":
            break
    return count


def _indents_from_list(version_list):
    """Given lines beginning with a varied number of spaces, return sorted list of number of spaces

    Args:
        version_list -- raw strings representing versions. For example:
            1.0.9.8.6 0
                500 http://security.debian.org/ jessie/updates/main amd64 Packages

    Returns:
        Sorted number of preceeding spaces for each level of input (e.g., [4, 8])
    """

    indents = set()
    for row in version_list:
        indents.add(_count_leading_spaces(row))

    return sorted(indents)

def _parse_version_table(raw_version_list):
    """Given test of version table, create version_list

    Args:
        raw_version_list -- raw multi-line string representating output of
            version table such as:
                Version table:
                   1.0.9.8.6 0
                      500 http://security.debian.org/ jessie/updates/main amd64 Packages
               *** 1.0.9.8.5 0
                      100 /var/lib/dpkg/status
                   1.0.9.8.4 0
                      500 http://httpredir.debian.org/debian/ jessie/main amd64 Packages

    Returns:
        A list of versions from first level indent such as:
            ["1.0.9.8.4", "1.0.9.8.5", "1.0.9.8.6"]

    """
    versions = []

    # Replacing any '***' in the lines
    version_list = [item.replace('*', ' ') for item in raw_version_list]

    spaces = _indents_from_list(version_list)
    assert len(spaces) >= 2  # Our assumptions from the input above

    version_level = spaces[0]
    for row in version_list:
        if _count_leading_spaces(row) == version_level:
            versions.append(row.strip().split()[0])

    return versions

def _fail_if_error(_ansible_module, cmd, return_code, err):
    """Fail the ansible module if there is an error or return code is non zero"""

    if return_code or err:
        _ansible_module.fail_json(
            msg="Executing command '%s' failed. rc: %s err: %s" % (
                cmd, return_code, err))

def parse_apt_cache_policy(content):
    """Given output of "apt-cache policy" return relevant fields (dict)

    Args:
        content -- raw multi-line string representating output of
                   apt-cache policy <package>

    Returns:
        A dictionary of relevant fields. For example:
            {'package_name': 'cowsay',
             'installed': '3.03+dfsg1-10',
             'candidate': '3.03+dfsg1-10'}

    Output of "apt-cache policy cowsay" (for example) looks like the
    following:
    cowsay:
      Installed: 3.03+dfsg1-10
      Candidate: 3.03+dfsg1-10
      Version table:
        ...

    Note #1: If no package is in the cache

    If the package being asked for is non-existant (e.g., foo),
    "apt-cache policy" doesn't return all four lines. Instead, one will see
    something similar to (with a successful return code):

    > $ apt-cache policy foo
    > N: Unable to locate package foo

    If there are less than four lines in the output, we will assume that this this
    package doesn't exit.

    Note #2: This module parsing is currently incredibly simple. The
             author wants to do a simple state parser, however, until we
             see output that needs it, we will stick with super simple.
    """
    results = {}
    package_name_idx = 0
    installed_idx = 1
    candidate_idx = 2
    version_table_idx = 3

    output = content.strip().split('\n')
    if len(output) >= 4:
        assert output[version_table_idx] == "  Version table:"
        results['package_name'] = output[package_name_idx].strip()[:-1]
        results['installed'] = output[installed_idx].replace("Installed: ", "").strip()
        results['candidate'] = output[candidate_idx].replace("Candidate: ", "").strip()
        results['versions'] = _parse_version_table(output[version_table_idx+1:])

    return results


def apt_cache_policy_info(_ansible_module, package_name):
    """Execute apt-cache policy and return results of relevent fields(dict)

    See parse_apt_cache_policy for more info.
    """
    cmd = "apt-cache policy %s" % package_name
    return_code, out, err = _ansible_module.run_command(cmd)
    _fail_if_error(_ansible_module, cmd, return_code, err)
    return parse_apt_cache_policy(out)


def dpkg_files(_ansible_module, package_name):
    """Given a package name, return list of files in package

    This is the equivalent of `dpkg-query -L <package_name>`
    """

    cmd = "dpkg-query -L %s" % package_name
    return_code, out, err = _ansible_module.run_command(cmd)
    _fail_if_error(_ansible_module, cmd, return_code, err)

    if "does not contain any files" in out:
      return []

    return out.strip().split('\n')


def package_status(_ansible_module, pkgname, version, state):
    """Determine package's currently installed status

    Parameters:
    pkgname (str): Package name in question
    version (str|None): Version of package to be installed (if provided)
    state (str): Desired state of package

    Returns (tuple):
    package_is_installed (bool)
    version_is_installed (bool)
    package_is_upgradable (bool)
    has_files (bool)
    """
    results = {
        'package_is_installed': False,
        'version_is_installed': False,
        'version_is_upgradable': False,
        'has_files': False
    }

    def is_pkg_installed(cache_info):
        """from apt-cache policy (apt_cache_policy_info)"""
        return 'installed' in cache_info and cache_info['installed'] != '(none)'


    def is_version_installed(version, cache_info):
        """Given version, check if it is installed from cache_info"""

        if version:
            return version == cache_info['installed']
        else:
            # Yes, this is weird. It's the logic built into the assumptions from when
            # we had very large try/except blocks using the python_apt library
            # Eventually this logic should be refactored. The first step is to remove
            # dependency upon python_apt library
            return True


    def available_upgrades(version, cache_info):
        """Given version and cache_info, return available upgrades

        Args:
            version -- intended version to install (string) (Example: '1.3.3.5-4')
            cache_info -- Dictionary representing output of `apt-cache policy <pkg>`
                       Note that the 'versions' order follows top-down of command output
                       Example: {'versions': ['1.3.3.5-4+deb8u7', '1.3.3.5-4'],
                                 'candidate': '1.3.3.5-4+deb8u7',
                                 'package_name': '389-ds-base',
                                 'installed': '(none)'}

        Returns:
            Any upgrade candidate from installed version "forward" input
            parameter 'version' (including version).
            For example (for given input examples): ['1.3.3.5-4']
        """

        _version_list = cache_info['versions'][::-1]

        if cache_info['installed'] == '(none)':
            start_idx = 0
        else:
            start_idx = _version_list.index(cache_info['installed'])

        if version:
            stop_idx = _version_list.index(version)
        else:
            stop_idx = len(_version_list)

        return _version_list[start_idx:stop_idx+1]


    def is_upgradable(version, cache_info):
        """Given version and package cache info return package is upgradable

        As far as the originally used 'python_apt' library was concerned, a
        package was not upgradable if not installed.

        > .../dist-packages/apt/package.py
        >     return (self.is_installed and
        >         self._pcache._depcache.is_upgradable(self._pkg))

        However, extra complexity related to provided version and if package is
        installed was added to the original source of this function. When
        refactoring to remove the python_apt library dependencies, the extra
        complexity regarding versions installed and a bool(avail_upgrades) was
        left in this function to preserve original behavior.

        Over time, we should consider simplifying this
        """
        package_installed = is_pkg_installed(cache_info)
        avail_upgrades = available_upgrades(version, cache_info)

        if version:
            if package_installed:
                if len(avail_upgrades) == 1 and avail_upgrades[0] == version:
                    return False
                return bool(avail_upgrades)
            else:
                upgradable = False
                for potential_version in avail_upgrades:
                    if version == potential_version:
                        upgradable = True
                return upgradable
        else:
            return package_installed and (
                cache_info['installed'] != cache_info['candidate'])


    def has_package_files(_ansible_module, package_name):
        """Given package_name, return True if package has files"""

        # If a package is not installed, failure will be handled by
        # _fail_if_error. Just like dpkg, requesting files for a not installed
        # is an error. Otherwise correctly return if the package (still) has
        # files.
        return any(dpkg_files(_ansible_module, package_name))

    cache_info = apt_cache_policy_info(_ansible_module, pkgname)
    if is_pkg_installed(cache_info):
        results['package_is_installed'] = True
        results['version_is_installed'] = is_version_installed(version, cache_info)
    else:
        results['package_is_installed'] = False
        results['version_is_installed'] = False

    results['package_is_upgradable'] = is_upgradable(version, cache_info)
    results['has_files'] = has_package_files(_ansible_module, pkgname)

    return results['package_is_installed'],\
           results['version_is_installed'],\
           results['version_is_upgradable'],\
           results['has_files']

#########################################
# END package_status (python_apt removal)
#########################################

def expand_dpkg_options(dpkg_options_compressed):
    options_list = dpkg_options_compressed.split(',')
    dpkg_options = ""
    for dpkg_option in options_list:
        dpkg_options = '%s -o "Dpkg::Options::=--%s"' \
                       % (dpkg_options, dpkg_option)
    return dpkg_options.strip()


def expand_pkgspec_from_fnmatches(m, pkgspec, cache):
    # Note: apt-get does implicit regex matching when an exact package name
    # match is not found.  Something like this:
    # matches = [pkg.name for pkg in cache if re.match(pkgspec, pkg.name)]
    # (Should also deal with the ':' for multiarch like the fnmatch code below)
    #
    # We have decided not to do similar implicit regex matching but might take
    # a PR to add some sort of explicit regex matching:
    # https://github.com/ansible/ansible-modules-core/issues/1258
    new_pkgspec = []
    if pkgspec:
        for pkgspec_pattern in pkgspec:
            pkgname_pattern, version = package_split(pkgspec_pattern)

            # note that none of these chars is allowed in a (debian) pkgname
            if frozenset('*?[]!').intersection(pkgname_pattern):
                # handle multiarch pkgnames, the idea is that "apt*" should
                # only select native packages. But "apt*:i386" should still work
                if ":" not in pkgname_pattern:
                    # Filter the multiarch packages from the cache only once
                    try:
                        pkg_name_cache = _non_multiarch
                    except NameError:
                        pkg_name_cache = _non_multiarch = [pkg.name for pkg in cache if ':' not in pkg.name]  # noqa: F841
                else:
                    # Create a cache of pkg_names including multiarch only once
                    try:
                        pkg_name_cache = _all_pkg_names
                    except NameError:
                        pkg_name_cache = _all_pkg_names = [pkg.name for pkg in cache]  # noqa: F841

                matches = fnmatch.filter(pkg_name_cache, pkgname_pattern)

                if not matches:
                    m.fail_json(msg="No package(s) matching '%s' available" % str(pkgname_pattern))
                else:
                    new_pkgspec.extend(matches)
            else:
                # No wildcards in name
                new_pkgspec.append(pkgspec_pattern)
    return new_pkgspec


def parse_diff(output):
    diff = to_native(output).splitlines()
    try:
        # check for start marker from aptitude
        diff_start = diff.index('Resolving dependencies...')
    except ValueError:
        try:
            # check for start marker from apt-get
            diff_start = diff.index('Reading state information...')
        except ValueError:
            # show everything
            diff_start = -1
    try:
        # check for end marker line from both apt-get and aptitude
        diff_end = next(i for i, item in enumerate(diff) if re.match('[0-9]+ (packages )?upgraded', item))
    except StopIteration:
        diff_end = len(diff)
    diff_start += 1
    diff_end += 1
    return {'prepared': '\n'.join(diff[diff_start:diff_end])}


def mark_installed_manually(m, packages):
    if not packages:
        return

    apt_mark_cmd_path = m.get_bin_path("apt-mark")

    # https://github.com/ansible/ansible/issues/40531
    if apt_mark_cmd_path is None:
        m.warn("Could not find apt-mark binary, not marking package(s) as manually installed.")
        return

    cmd = "%s manual %s" % (apt_mark_cmd_path, ' '.join(packages))
    rc, out, err = m.run_command(cmd)

    if APT_MARK_INVALID_OP in err or APT_MARK_INVALID_OP_DEB6 in err:
        cmd = "%s unmarkauto %s" % (apt_mark_cmd_path, ' '.join(packages))
        rc, out, err = m.run_command(cmd)

    if rc != 0:
        m.fail_json(msg="'%s' failed: %s" % (cmd, err), stdout=out, stderr=err, rc=rc)


def install(m, pkgspec, cache, upgrade=False, default_release=None,
            install_recommends=None, force=False,
            dpkg_options=expand_dpkg_options(DPKG_OPTIONS),
            build_dep=False, fixed=False, autoremove=False, only_upgrade=False,
            allow_unauthenticated=False):
    pkg_list = []
    packages = ""
    pkgspec = expand_pkgspec_from_fnmatches(m, pkgspec, cache)
    package_names = []
    for package in pkgspec:
        if build_dep:
            # Let apt decide what to install
            pkg_list.append("'%s'" % package)
            continue

        name, version = package_split(package)
        package_names.append(name)
        installed, installed_version, upgradable, has_files = package_status(m, name, version, state='install')
        if (not installed and not only_upgrade) or (installed and not installed_version) or (upgrade and upgradable):
            pkg_list.append("'%s'" % package)
        if installed_version and upgradable and version:
            # This happens when the package is installed, a newer version is
            # available, and the version is a wildcard that matches both
            #
            # We do not apply the upgrade flag because we cannot specify both
            # a version and state=latest.  (This behaviour mirrors how apt
            # treats a version with wildcard in the package)
            pkg_list.append("'%s'" % package)
    packages = ' '.join(pkg_list)

    if packages:
        if force:
            force_yes = '--force-yes'
        else:
            force_yes = ''

        if m.check_mode:
            check_arg = '--simulate'
        else:
            check_arg = ''

        if autoremove:
            autoremove = '--auto-remove'
        else:
            autoremove = ''

        if only_upgrade:
            only_upgrade = '--only-upgrade'
        else:
            only_upgrade = ''

        if fixed:
            fixed = '--fix-broken'
        else:
            fixed = ''

        if build_dep:
            cmd = "%s -y %s %s %s %s %s build-dep %s" % (APT_GET_CMD, dpkg_options, only_upgrade, fixed, force_yes, check_arg, packages)
        else:
            cmd = "%s -y %s %s %s %s %s %s install %s" % (APT_GET_CMD, dpkg_options, only_upgrade, fixed, force_yes, autoremove, check_arg, packages)

        if default_release:
            cmd += " -t '%s'" % (default_release,)

        if install_recommends is False:
            cmd += " -o APT::Install-Recommends=no"
        elif install_recommends is True:
            cmd += " -o APT::Install-Recommends=yes"
        # install_recommends is None uses the OS default

        if allow_unauthenticated:
            cmd += " --allow-unauthenticated"

        with PolicyRcD(m):
            rc, out, err = m.run_command(cmd)

        if m._diff:
            diff = parse_diff(out)
        else:
            diff = {}
        status = True

        changed = True
        if build_dep:
            changed = APT_GET_ZERO not in out

        data = dict(changed=changed, stdout=out, stderr=err, diff=diff)
        if rc:
            status = False
            data = dict(msg="'%s' failed: %s" % (cmd, err), stdout=out, stderr=err, rc=rc)
    else:
        status = True
        data = dict(changed=False)

    if not build_dep:
        mark_installed_manually(m, package_names)

    return (status, data)


def get_field_of_deb(m, deb_file, field="Version"):
    cmd_dpkg = m.get_bin_path("dpkg", True)
    cmd = cmd_dpkg + " --field %s %s" % (deb_file, field)
    rc, stdout, stderr = m.run_command(cmd)
    if rc != 0:
        m.fail_json(msg="%s failed" % cmd, stdout=stdout, stderr=stderr)
    return to_native(stdout).strip('\n')


def install_deb(m, debs, cache, force, install_recommends, allow_unauthenticated, dpkg_options):
    changed = False
    deps_to_install = []
    pkgs_to_install = []
    for deb_file in debs.split(','):
        try:
            pkg = apt.debfile.DebPackage(deb_file)
            pkg_name = get_field_of_deb(m, deb_file, "Package")
            pkg_version = get_field_of_deb(m, deb_file, "Version")
            if len(apt_pkg.get_architectures()) > 1:
                pkg_arch = get_field_of_deb(m, deb_file, "Architecture")
                pkg_key = "%s:%s" % (pkg_name, pkg_arch)
            else:
                pkg_key = pkg_name
            try:
                installed_pkg = apt.Cache()[pkg_key]
                installed_version = installed_pkg.installed.version
                if package_version_compare(pkg_version, installed_version) == 0:
                    # Does not need to down-/upgrade, move on to next package
                    continue
            except Exception:
                # Must not be installed, continue with installation
                pass
            # Check if package is installable
            if not pkg.check() and not force:
                m.fail_json(msg=pkg._failure_string)

            # add any missing deps to the list of deps we need
            # to install so they're all done in one shot
            deps_to_install.extend(pkg.missing_deps)

        except Exception as e:
            m.fail_json(msg="Unable to install package: %s" % to_native(e))

        # and add this deb to the list of packages to install
        pkgs_to_install.append(deb_file)

    # install the deps through apt
    retvals = {}
    if deps_to_install:
        (success, retvals) = install(m=m, pkgspec=deps_to_install, cache=cache,
                                     install_recommends=install_recommends,
                                     allow_unauthenticated=allow_unauthenticated,
                                     dpkg_options=expand_dpkg_options(dpkg_options))
        if not success:
            m.fail_json(**retvals)
        changed = retvals.get('changed', False)

    if pkgs_to_install:
        options = ' '.join(["--%s" % x for x in dpkg_options.split(",")])
        if m.check_mode:
            options += " --simulate"
        if force:
            options += " --force-all"

        cmd = "dpkg %s -i %s" % (options, " ".join(pkgs_to_install))

        with PolicyRcD(m):
            rc, out, err = m.run_command(cmd)

        if "stdout" in retvals:
            stdout = retvals["stdout"] + out
        else:
            stdout = out
        if "diff" in retvals:
            diff = retvals["diff"]
            if 'prepared' in diff:
                diff['prepared'] += '\n\n' + out
        else:
            diff = parse_diff(out)
        if "stderr" in retvals:
            stderr = retvals["stderr"] + err
        else:
            stderr = err

        if rc == 0:
            m.exit_json(changed=True, stdout=stdout, stderr=stderr, diff=diff)
        else:
            m.fail_json(msg="%s failed" % cmd, stdout=stdout, stderr=stderr)
    else:
        m.exit_json(changed=changed, stdout=retvals.get('stdout', ''), stderr=retvals.get('stderr', ''), diff=retvals.get('diff', ''))


def remove(m, pkgspec, cache, purge=False, force=False,
           dpkg_options=expand_dpkg_options(DPKG_OPTIONS), autoremove=False):
    pkg_list = []
    pkgspec = expand_pkgspec_from_fnmatches(m, pkgspec, cache)
    for package in pkgspec:
        name, version = package_split(package)
        installed, installed_version, upgradable, has_files = package_status(m, name, version, state='remove')
        if installed_version or (has_files and purge):
            pkg_list.append("'%s'" % package)
    packages = ' '.join(pkg_list)

    if not packages:
        m.exit_json(changed=False)
    else:
        if force:
            force_yes = '--force-yes'
        else:
            force_yes = ''

        if purge:
            purge = '--purge'
        else:
            purge = ''

        if autoremove:
            autoremove = '--auto-remove'
        else:
            autoremove = ''

        if m.check_mode:
            check_arg = '--simulate'
        else:
            check_arg = ''

        cmd = "%s -q -y %s %s %s %s %s remove %s" % (APT_GET_CMD, dpkg_options, purge, force_yes, autoremove, check_arg, packages)

        with PolicyRcD(m):
            rc, out, err = m.run_command(cmd)

        if m._diff:
            diff = parse_diff(out)
        else:
            diff = {}
        if rc:
            m.fail_json(msg="'apt-get remove %s' failed: %s" % (packages, err), stdout=out, stderr=err, rc=rc)
        m.exit_json(changed=True, stdout=out, stderr=err, diff=diff)


def cleanup(m, purge=False, force=False, operation=None,
            dpkg_options=expand_dpkg_options(DPKG_OPTIONS)):

    if operation not in frozenset(['autoremove', 'autoclean']):
        raise AssertionError('Expected "autoremove" or "autoclean" cleanup operation, got %s' % operation)

    if force:
        force_yes = '--force-yes'
    else:
        force_yes = ''

    if purge:
        purge = '--purge'
    else:
        purge = ''

    if m.check_mode:
        check_arg = '--simulate'
    else:
        check_arg = ''

    cmd = "%s -y %s %s %s %s %s" % (APT_GET_CMD, dpkg_options, purge, force_yes, operation, check_arg)

    with PolicyRcD(m):
        rc, out, err = m.run_command(cmd)

    if m._diff:
        diff = parse_diff(out)
    else:
        diff = {}
    if rc:
        m.fail_json(msg="'apt-get %s' failed: %s" % (operation, err), stdout=out, stderr=err, rc=rc)

    changed = CLEAN_OP_CHANGED_STR[operation] in out

    m.exit_json(changed=changed, stdout=out, stderr=err, diff=diff)


def upgrade(m, mode="yes", force=False, default_release=None,
            use_apt_get=False,
            dpkg_options=expand_dpkg_options(DPKG_OPTIONS), autoremove=False,
            allow_unauthenticated=False,
            ):

    if autoremove:
        autoremove = '--auto-remove'
    else:
        autoremove = ''

    if m.check_mode:
        check_arg = '--simulate'
    else:
        check_arg = ''

    apt_cmd = None
    prompt_regex = None
    if mode == "dist" or (mode == "full" and use_apt_get):
        # apt-get dist-upgrade
        apt_cmd = APT_GET_CMD
        upgrade_command = "dist-upgrade %s" % (autoremove)
    elif mode == "full" and not use_apt_get:
        # aptitude full-upgrade
        apt_cmd = APTITUDE_CMD
        upgrade_command = "full-upgrade"
    else:
        if use_apt_get:
            apt_cmd = APT_GET_CMD
            upgrade_command = "upgrade --with-new-pkgs %s" % (autoremove)
        else:
            # aptitude safe-upgrade # mode=yes # default
            apt_cmd = APTITUDE_CMD
            upgrade_command = "safe-upgrade"
            prompt_regex = r"(^Do you want to ignore this warning and proceed anyway\?|^\*\*\*.*\[default=.*\])"

    if force:
        if apt_cmd == APT_GET_CMD:
            force_yes = '--force-yes'
        else:
            force_yes = '--assume-yes --allow-untrusted'
    else:
        force_yes = ''

    allow_unauthenticated = '--allow-unauthenticated' if allow_unauthenticated else ''

    if apt_cmd is None:
        if use_apt_get:
            apt_cmd = APT_GET_CMD
        else:
            m.fail_json(msg="Unable to find APTITUDE in path. Please make sure "
                            "to have APTITUDE in path or use 'force_apt_get=True'")
    apt_cmd_path = m.get_bin_path(apt_cmd, required=True)

    cmd = '%s -y %s %s %s %s %s' % (apt_cmd_path, dpkg_options, force_yes, allow_unauthenticated,
                                    check_arg, upgrade_command)

    if default_release:
        cmd += " -t '%s'" % (default_release,)

    with PolicyRcD(m):
        rc, out, err = m.run_command(cmd, prompt_regex=prompt_regex)

    if m._diff:
        diff = parse_diff(out)
    else:
        diff = {}
    if rc:
        m.fail_json(msg="'%s %s' failed: %s" % (apt_cmd, upgrade_command, err), stdout=out, rc=rc)
    if (apt_cmd == APT_GET_CMD and APT_GET_ZERO in out) or (apt_cmd == APTITUDE_CMD and APTITUDE_ZERO in out):
        m.exit_json(changed=False, msg=out, stdout=out, stderr=err)
    m.exit_json(changed=True, msg=out, stdout=out, stderr=err, diff=diff)


def get_cache_mtime():
    """Return mtime of a valid apt cache file.
    Stat the apt cache file and if no cache file is found return 0
    :returns: ``int``
    """
    cache_time = 0
    if os.path.exists(APT_UPDATE_SUCCESS_STAMP_PATH):
        cache_time = os.stat(APT_UPDATE_SUCCESS_STAMP_PATH).st_mtime
    elif os.path.exists(APT_LISTS_PATH):
        cache_time = os.stat(APT_LISTS_PATH).st_mtime
    return cache_time


def get_updated_cache_time():
    """Return the mtime time stamp and the updated cache time.
    Always retrieve the mtime of the apt cache or set the `cache_mtime`
    variable to 0
    :returns: ``tuple``
    """
    cache_mtime = get_cache_mtime()
    mtimestamp = datetime.datetime.fromtimestamp(cache_mtime)
    updated_cache_time = int(time.mktime(mtimestamp.timetuple()))
    return mtimestamp, updated_cache_time


# https://github.com/ansible/ansible-modules-core/issues/2951
def get_cache(module):
    '''Attempt to get the cache object and update till it works'''
    cache = None
    try:
        cache = apt.Cache()
    except SystemError as e:
        if '/var/lib/apt/lists/' in to_native(e).lower():
            # update cache until files are fixed or retries exceeded
            retries = 0
            while retries < 2:
                (rc, so, se) = module.run_command(['apt-get', 'update', '-q'])
                retries += 1
                if rc == 0:
                    break
            if rc != 0:
                module.fail_json(msg='Updating the cache to correct corrupt package lists failed:\n%s\n%s' % (to_native(e), so + se), rc=rc)
            # try again
            cache = apt.Cache()
        else:
            module.fail_json(msg=to_native(e))
    return cache


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', default='present', choices=['absent', 'build-dep', 'fixed', 'latest', 'present']),
            update_cache=dict(type='bool', aliases=['update-cache']),
            cache_valid_time=dict(type='int', default=0),
            purge=dict(type='bool', default=False),
            package=dict(type='list', aliases=['pkg', 'name']),
            deb=dict(type='path'),
            default_release=dict(type='str', aliases=['default-release']),
            install_recommends=dict(type='bool', aliases=['install-recommends']),
            force=dict(type='bool', default=False),
            upgrade=dict(type='str', choices=['dist', 'full', 'no', 'safe', 'yes']),
            dpkg_options=dict(type='str', default=DPKG_OPTIONS),
            autoremove=dict(type='bool', default=False),
            autoclean=dict(type='bool', default=False),
            policy_rc_d=dict(type='int', default=None),
            only_upgrade=dict(type='bool', default=False),
            force_apt_get=dict(type='bool', default=False),
            allow_unauthenticated=dict(type='bool', default=False, aliases=['allow-unauthenticated']),
        ),
        mutually_exclusive=[['deb', 'package', 'upgrade']],
        required_one_of=[['autoremove', 'deb', 'package', 'update_cache', 'upgrade']],
        supports_check_mode=True,
    )

    module.run_command_environ_update = APT_ENV_VARS

    # CODE REMOVED HERE

    global APTITUDE_CMD
    APTITUDE_CMD = module.get_bin_path("aptitude", False)
    global APT_GET_CMD
    APT_GET_CMD = module.get_bin_path("apt-get")

    p = module.params

    if p['upgrade'] == 'no':
        p['upgrade'] = None

    use_apt_get = p['force_apt_get']

    if not use_apt_get and not APTITUDE_CMD:
        use_apt_get = True

    updated_cache = False
    updated_cache_time = 0
    install_recommends = p['install_recommends']
    allow_unauthenticated = p['allow_unauthenticated']
    dpkg_options = expand_dpkg_options(p['dpkg_options'])
    autoremove = p['autoremove']
    autoclean = p['autoclean']

    # Get the cache object
    cache = get_cache(module)

    try:
        if p['default_release']:
            try:
                apt_pkg.config['APT::Default-Release'] = p['default_release']
            except AttributeError:
                apt_pkg.Config['APT::Default-Release'] = p['default_release']
            # reopen cache w/ modified config
            cache.open(progress=None)

        mtimestamp, updated_cache_time = get_updated_cache_time()
        # Cache valid time is default 0, which will update the cache if
        #  needed and `update_cache` was set to true
        updated_cache = False
        if p['update_cache'] or p['cache_valid_time']:
            now = datetime.datetime.now()
            tdelta = datetime.timedelta(seconds=p['cache_valid_time'])
            if not mtimestamp + tdelta >= now:
                # Retry to update the cache up to 3 times
                err = ''
                for retry in range(3):
                    try:
                        cache.update()
                        break
                    except apt.cache.FetchFailedException as e:
                        err = to_native(e)
                else:
                    module.fail_json(msg='Failed to update apt cache: %s' % err)
                cache.open(progress=None)
                mtimestamp, post_cache_update_time = get_updated_cache_time()
                if updated_cache_time != post_cache_update_time:
                    updated_cache = True
                updated_cache_time = post_cache_update_time

            # If there is nothing else to do exit. This will set state as
            #  changed based on if the cache was updated.
            if not p['package'] and not p['upgrade'] and not p['deb']:
                module.exit_json(
                    changed=updated_cache,
                    cache_updated=updated_cache,
                    cache_update_time=updated_cache_time
                )

        force_yes = p['force']

        if p['upgrade']:
            upgrade(module, p['upgrade'], force_yes, p['default_release'], use_apt_get, dpkg_options, autoremove, allow_unauthenticated)

        if p['deb']:
            if p['state'] != 'present':
                module.fail_json(msg="deb only supports state=present")
            if '://' in p['deb']:
                p['deb'] = fetch_file(module, p['deb'])
            install_deb(module, p['deb'], cache,
                        install_recommends=install_recommends,
                        allow_unauthenticated=allow_unauthenticated,
                        force=force_yes, dpkg_options=p['dpkg_options'])

        unfiltered_packages = p['package'] or ()
        packages = [package.strip() for package in unfiltered_packages if package != '*']
        all_installed = '*' in unfiltered_packages
        latest = p['state'] == 'latest'

        if latest and all_installed:
            if packages:
                module.fail_json(msg='unable to install additional packages when upgrading all installed packages')
            upgrade(module, 'yes', force_yes, p['default_release'], use_apt_get, dpkg_options, autoremove, allow_unauthenticated)

        if packages:
            for package in packages:
                if package.count('=') > 1:
                    module.fail_json(msg="invalid package spec: %s" % package)
                if latest and '=' in package:
                    module.fail_json(msg='version number inconsistent with state=latest: %s' % package)

        if not packages:
            if autoclean:
                cleanup(module, p['purge'], force=force_yes, operation='autoclean', dpkg_options=dpkg_options)
            if autoremove:
                cleanup(module, p['purge'], force=force_yes, operation='autoremove', dpkg_options=dpkg_options)

        if p['state'] in ('latest', 'present', 'build-dep', 'fixed'):
            state_upgrade = False
            state_builddep = False
            state_fixed = False
            if p['state'] == 'latest':
                state_upgrade = True
            if p['state'] == 'build-dep':
                state_builddep = True
            if p['state'] == 'fixed':
                state_fixed = True

            success, retvals = install(
                module,
                packages,
                cache,
                upgrade=state_upgrade,
                default_release=p['default_release'],
                install_recommends=install_recommends,
                force=force_yes,
                dpkg_options=dpkg_options,
                build_dep=state_builddep,
                fixed=state_fixed,
                autoremove=autoremove,
                only_upgrade=p['only_upgrade'],
                allow_unauthenticated=allow_unauthenticated
            )

            # Store if the cache has been updated
            retvals['cache_updated'] = updated_cache
            # Store when the update time was last
            retvals['cache_update_time'] = updated_cache_time

            if success:
                module.exit_json(**retvals)
            else:
                module.fail_json(**retvals)
        elif p['state'] == 'absent':
            remove(module, packages, cache, p['purge'], force=force_yes, dpkg_options=dpkg_options, autoremove=autoremove)

    except apt.cache.LockFailedException:
        module.fail_json(msg="Failed to lock apt for exclusive operation")
    except apt.cache.FetchFailedException:
        module.fail_json(msg="Could not fetch updated apt files")


if __name__ == "__main__":
    main()
