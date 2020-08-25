clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

rebuild: ## Rebuild Debian box for testing
	vagrant destroy -f
	vagrant up

fetch: ## Fetch files from Vagrant box for faster development cycle
	# Requires vagrant scp module
        # These failes are temporarily created on Vagrant box during
        # testing and/or development
	vagrant scp default:/vagrant/ansible.cfg .
	vagrant scp default:/vagrant/modules/sapt.py modules/sapt.py
	vagrant scp default:/vagrant/run_test.sh run_test.sh
	vagrant scp default:/vagrant/RESULTS_add.txt RESULTS_add.txt

test_run: rebuild
	vagrant scp default:/tmp/test_results.txt tmp_results.txt
	cat tmp_results.txt >> RESULTS.txt
	rm tmp_results.txt
