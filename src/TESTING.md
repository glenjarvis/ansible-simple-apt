# Testing

## Objective

In an effort to ensure we keep the same behavior, we wish to test the same
behavior that is current so that we can compare our fork with the original
results.

There are several variables that need to be tested:

* Operating System
  Possible values include:
    - Wheezy (Debian 7)
    - Jessie (Debian 8)
    - Stretch (Debian 9)
    - Buster (Debian 10)
    - Bullseye (Debian 11)
    - An Ubuntu variant
    - More variants not listed

* Apt package name
  Ideally, this is a package that contains more than one version for other
  upgrade/downgrade tests.
  For example, on Jessie (Debian 7), there is a package named `389-ds-base`
  It has two versions (1.3.3.5-4 and 1.3.3.5-4+deb8u7) in its version table:

```
    Version table:
    *** 1.3.3.5-4+deb8u7 0
          500 http://security.debian.org/ jessie/updates/main amd64 Packages
          100 /var/lib/dpkg/status
        1.3.3.5-4 0
          500 http://httpredir.debian.org/debian/ jessie/main amd64 Packages
```

* Package version
  Possible examples per the details above:
    - None (No current version is installed)
    - 1.3.3.5-4
    - 1.3.3.5-4+deb8u7

* Ansible requested state
  Possible values:
    - absent
    - present
    - latest
    - build-dep
    - fixed


## Current Testing Grid

|Test |  OS   |Prev install| Previous Version | Package Name                 |  Ansible State
|-----|-------|------------|------------------|------------------------------|----------------
|08-01|jesse  |     No     |   N/A            | 389-ds-base                  |   absent
|08-02|jesse  |     No     |   N/A            | 389-ds-base                  |   build-dep
|08-03|jesse  |     No     |   N/A            | 389-ds-base                  |   fixed
|08-04|jesse  |     No     |   N/A            | 389-ds-base                  |   latest
|08-05|jesse  |     No     |   N/A            | 389-ds-base                  |   present
|08-06|jesse  |     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   absent
|08-07|jesse  |     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   build-dep
|08-08|jesse  |     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   fixed
|08-09|jesse  |     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   latest
|08-10|jesse  |     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   present
|08-11|jesse  |     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   absent
|08-12|jesse  |     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   build-dep
|08-13|jesse  |     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   fixed
|08-14|jesse  |     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   latest
|08-15|jesse  |     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   present
|08-16|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base                  |   absent
|08-17|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base                  |   build-dep
|08-18|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base                  |   fixed
|08-19|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base                  |   latest
|08-20|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base                  |   present
|08-21|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   absent
|08-22|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   build-dep
|08-23|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   fixed
|08-24|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   latest
|08-25|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   present
|08-26|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   absent
|08-27|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   build-dep
|08-28|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   fixed
|08-29|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   latest
|08-30|jesse  |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   present
|08-31|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   absent
|08-32|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   build-dep
|08-33|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   fixed
|08-34|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   latest
|08-35|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   present
|08-36|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   absent
|08-37|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   build-dep
|08-38|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   fixed
|08-39|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   latest
|08-40|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   present
|08-41|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   absent
|08-42|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   build-dep
|08-43|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   fixed
|08-44|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   latest
|08-45|jesse  |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   present
|08-46|jesse  |     No     |   N/A            | completely-nonexistent-pkg   |   absent
|08-47|jesse  |     No     |   N/A            | completely-nonexistent-pkg   |   build-dep
|08-48|jesse  |     No     |   N/A            | completely-nonexistent-pkg   |   fixed
|08-49|jesse  |     No     |   N/A            | completely-nonexistent-pkg   |   latest
|08-50|jesse  |     No     |   N/A            | completely-nonexistent-pkg   |   present
|09-01|stretch|     No     |   N/A            | 389-ds-base                  |   absent
|09-02|stretch|     No     |   N/A            | 389-ds-base                  |   build-dep
|09-03|stretch|     No     |   N/A            | 389-ds-base                  |   fixed
|09-04|stretch|     No     |   N/A            | 389-ds-base                  |   latest
|09-05|stretch|     No     |   N/A            | 389-ds-base                  |   present
|09-06|stretch|     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   absent
|09-07|stretch|     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   build-dep
|09-08|stretch|     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   fixed
|09-09|stretch|     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   latest
|09-10|stretch|     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   present
|09-11|stretch|     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   absent
|09-12|stretch|     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   build-dep
|09-13|stretch|     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   fixed
|09-14|stretch|     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   latest
|09-15|stretch|     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   present
|09-16|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base                  |   absent
|09-17|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base                  |   build-dep
|09-18|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base                  |   fixed
|09-19|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base                  |   latest
|09-20|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base                  |   present
|09-21|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   absent
|09-22|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   build-dep
|09-23|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   fixed
|09-24|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   latest
|09-25|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   present
|09-26|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   absent
|09-27|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   build-dep
|09-28|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   fixed
|09-29|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   latest
|09-30|stretch|     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   present
|09-31|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   absent
|09-32|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   build-dep
|09-33|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   fixed
|09-34|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   latest
|09-35|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   present
|09-36|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   absent
|09-37|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   build-dep
|09-38|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   fixed
|09-39|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   latest
|09-40|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   present
|09-41|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   absent
|09-42|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   build-dep
|09-43|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   fixed
|09-44|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   latest
|09-45|stretch|     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   present
|09-46|stretch|     No     |   N/A            | completely-nonexistent-pkg   |   absent
|09-47|stretch|     No     |   N/A            | completely-nonexistent-pkg   |   build-dep
|09-48|stretch|     No     |   N/A            | completely-nonexistent-pkg   |   fixed
|09-49|stretch|     No     |   N/A            | completely-nonexistent-pkg   |   latest
|09-50|stretch|     No     |   N/A            | completely-nonexistent-pkg   |   present
|10-01|buster |     No     |   N/A            | 389-ds-base                  |   absent
|10-02|buster |     No     |   N/A            | 389-ds-base                  |   build-dep
|10-03|buster |     No     |   N/A            | 389-ds-base                  |   fixed
|10-04|buster |     No     |   N/A            | 389-ds-base                  |   latest
|10-05|buster |     No     |   N/A            | 389-ds-base                  |   present
|10-06|buster |     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   absent
|10-07|buster |     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   build-dep
|10-08|buster |     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   fixed
|10-09|buster |     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   latest
|10-10|buster |     No     |   N/A            | 389-ds-base=1.3.3.5-4        |   present
|10-11|buster |     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   absent
|10-12|buster |     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   build-dep
|10-13|buster |     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   fixed
|10-14|buster |     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   latest
|10-15|buster |     No     |   N/A            | 389-ds-base=1.3.3.5-4+deb8u7 |   present
|10-16|buster |     Yes    | 1.3.3.5-4        | 389-ds-base                  |   absent
|10-17|buster |     Yes    | 1.3.3.5-4        | 389-ds-base                  |   build-dep
|10-18|buster |     Yes    | 1.3.3.5-4        | 389-ds-base                  |   fixed
|10-19|buster |     Yes    | 1.3.3.5-4        | 389-ds-base                  |   latest
|10-20|buster |     Yes    | 1.3.3.5-4        | 389-ds-base                  |   present
|10-21|buster |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   absent
|10-22|buster |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   build-dep
|10-23|buster |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   fixed
|10-24|buster |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   latest
|10-25|buster |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4        |   present
|10-26|buster |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   absent
|10-27|buster |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   build-dep
|10-28|buster |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   fixed
|10-29|buster |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   latest
|10-30|buster |     Yes    | 1.3.3.5-4        | 389-ds-base=1.3.3.5-4+deb8u7 |   present
|10-31|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   absent
|10-32|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   build-dep
|10-33|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   fixed
|10-34|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   latest
|10-35|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base                  |   present
|10-36|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   absent
|10-37|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   build-dep
|10-38|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   fixed
|10-39|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   latest
|10-40|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4        |   present
|10-41|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   absent
|10-42|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   build-dep
|10-43|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   fixed
|10-44|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   latest
|10-45|buster |     Yes    | 1.3.3.5-4+deb8u7 | 389-ds-base=1.3.3.5-4+deb8u7 |   present
|10-46|buster |     No     |   N/A            | completely-nonexistent-pkg   |   absent
|10-47|buster |     No     |   N/A            | completely-nonexistent-pkg   |   build-dep
|10-48|buster |     No     |   N/A            | completely-nonexistent-pkg   |   fixed
|10-49|buster |     No     |   N/A            | completely-nonexistent-pkg   |   latest
|10-50|buster |     No     |   N/A            | completely-nonexistent-pkg   |   present

## Automatic Testing Framework

Although not the focus of the current iteration, we needed automated testing in
order to retain the same behavior between the **python_apt** library (pre-fork)
version and the **python_apt**-free (post-fork) version of the app.

Although the tools are rough and semi-automated, these are the conventions that
are currently in place.

As this becomes easier to manage, this will be the full automated testing
suite.

1. Test suite as data structure. Although not yet part of this repository, that
   datastructure is simlar to:

```
TEST_DATA = [
    {'test_num': '08-01',
     'os': 'jesse',
     'previously_installed': 'no',
     'previous_version': 'N/A',
     'package_name': '389-ds-base',
     'ansible_state': 'absent',
     'setup': 'setup_package_has_old_version_installed'},
...
    {'test_num': '10-50',
     'os': 'buster',
     'previously_installed': 'no',
     'previous_version': 'N/A',
     'package_name': 'completely-nonexistent-pkg',
     'ansible_state': 'present',
     'setup': 'setup_package_is_not_installed'},
]
````

2. Automated creation of `Vagrantfile`. Specifically, the `config.vm.box`
   parameter needs to be set to the operating system as given by the testing data
   above. For example: `config.vm.box = "debian/jessie64"`

   Also, note the provision 'shell' in the vagrant file used for doing
   automated testing:

   ```
   config.vm.provision "shell" do |p|
     p.inline = "/vagrant/run_test.sh"
   end
   ```

   This is the hook for the following steps.

3. Automated creation of `run_test.sh`. This is currently a template containing
   new_box_setup bash function and all setup functions.

   For example, here is a sample setup function for tests that have an "old
   version" of "389-ds-base" installed on Jesse.

   ```
   function setup_package_has_old_version_installed {
     sudo apt-get install -y 389-ds-base-libs=1.3.3.5-4 || true
     sudo apt-get install -y 389-ds-base=1.3.3.5-4 || true
   }
   ```

   Futher, this script:

   * Sets-up capturing output to a file (i.e, `/tmp/test_results.txt`)

   * Calls the appropriate setup function as provided by the test data in step 1

   * Prints the `apt-cache policy` of the package (to confirm setup from setup
     function but before test has been run). This is useful when reviewing test
     results in detail.

   * Prints the output of the `run_test_case.yml` playbook that is dynamically
     generated in step 4 below. This is also useful when reviewing test resutls
     in detail.

   * Calls `ansible-playbook`  on the dynamically created test playbook
     `run_test_case.yml` just mentioned.

   Specifically, the parts that are dynamically generated are:

   * The call to the appropriate setup function as provided by the test data
     for this test (e.g., `setup_package_has_old_version_installed`)

4. Automated creation of `run_test_case.yml`. This is the playbook that will be
   executed by the `run_test.sh` script mentioned in step 3. This is also templated. An example of a playbook is:

```
---
- name: Testing Playbook
  hosts: localhost
  tasks:
    - debug: msg="Ansible is working."

- name: Run test
  hosts: localhost
  tasks:
    - name: Run this test case
      sapt:
        name: 389-ds-base=1.3.3.5-4+deb8u7
        state: present
      become: yes
```

   Specifically, the parts that change are:

   * The **package_name** field provided by the test data
     (e.g., '**389-ds-base=1.3.3.5-4+deb8u7**')

   * The **ansible_state** field provided by the test data
     (e.g., '**present**')

5. Triggering of the execution of the test case. Once the temporary files
   previously mentioned are created (this part semi-manual-automated), the test
   case is triggered by calling `make test_run`.

   This rebuilds the Vagrant box (triggering the OS build and the provisioning
   of the `run_test.sh` script). The temporary files in the filesystem are
   automatically rsync'd to `/vagrant` on the Vagrant box being created.

   The `run_test.sh` script triggers running in this location with these files.

6. Copying relevant files from vagrant box (requires vagrant scp to also be
   installed). The `make fetch` command is used to fetch the appropriate files
   from the Vagrant box.

   Note that the `run_test.sh` script writes relevant infromation to temporary
   file `/tmp/test_results.txt`. The file is also fetched.

   This data is concatenated into the RESULTS.txt file for the test being run

7. Post processing of files. This part is mostly manual at the moment. There is
   noise in the `/tmp/test_results.txt` that is currently useful for debugging
   but noisy.


An example of a suite/range of tests is currenly done similar to:

```
def test_suite():
    """Begin Test Suite"""
    for row in TEST_DATA[0:15]:
        # [snipped] Append some boiler plate into RESULTS.txt
        os.system('make test_run')
```
