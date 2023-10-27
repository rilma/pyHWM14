
install-gfortran:
	sudo apt update -y
	sudp apt -y install gfortran

install:
	pip -q install coveralls
	pip install numpy
	pip install -e .

test:
	coverage run --source=. --module unittest discover --start-directory tests --verbose
