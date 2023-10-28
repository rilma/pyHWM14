
install-gfortran:
	sudo apt-get update -y
	sudo apt-get -y install gfortran

install:
	pip install coveralls numpy
	pip install -e .

test:
	coverage run --source=. --module unittest discover --start-directory tests --verbose
