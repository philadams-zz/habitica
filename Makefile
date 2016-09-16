.DEFAULT_GOAL := help

# display project help
help:
	cat README.md | head -n5

# run our roundup tests
#test:
#	cd ./tests; sh ./test

# register with pypi
register:
	python setup.py register

# prepare pypi distribution package
package:
	python setup.py sdist

# distribute on pypi
distribute:
	python setup.py sdist upload

# pep8 everything under /habitica
pep8:
	pep8 */*.py

# remove .pyc files
clean:
	rm */*.pyc
