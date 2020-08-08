function new_box_setup {
    sudo apt-get update
    sudo apt-get remove -y cowsay
}

function setup_package_has_old_version_installed {
  sudo apt-get install -y 389-ds-base-libs=1.3.3.5-4 || true
  sudo apt-get install -y 389-ds-base=1.3.3.5-4 || true
}

function setup_package_has_new_version_installed {
  sudo apt-get install -y 389-ds-base-libs=1.3.3.5-4+deb8u7 || true
  sudo apt-get install -y 389-ds-base=1.3.3.5-4+deb8u7 || true
}

function setup_package_is_not_installed {
    echo "Setting up 'setup_previous_package_version'"
    sudo apt-get remove -y 389-ds-base-libs=1.3.3.5-4 || true
    sudo apt-get automremove -y 389-ds-base-libs=1.3.3.5-4 || true
    sudo apt-get remove -y 389-ds-base=1.3.3.5-4 || true
    sudo apt-get autoremove -y 389-ds-base=1.3.3.5-4 || true
}

new_box_setup
#setup_package_is_not_installed
#setup_package_has_old_version_installed
setup_package_has_new_version_installed

sudo cat /dev/null > /tmp/test_results.txt
sudo chmod 777 /tmp/test_results.txt
echo "===================================" >> /tmp/test_results.txt
echo "|test_num | package_is_installed, version_is_installed, package_is_upgradable, has_files"
echo "+---------+------+------------+------------------+------------------------------+----------------"
apt-cache policy 389-ds-base | tee -a /tmp/test_results.txt
cat ./run_test_case.yml | tee -a /tmp/test_results.txt
ansible-playbook run_test_case.yml | tee -a /tmp/test_results.txt

