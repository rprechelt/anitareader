##
# anitareader
#
# @file
# @version 0.0.1

# our testing targets
.PHONY: tests flake black mypy all

all: mypy isort black flake tests

tests:
	python -m pytest --cov=anitareader tests

flake:
	python -m flake8 anitareader

black:
	python -m black -t py37 anitareader tests

mypy:
	python -m mypy anitareader

isort:
	python -m isort --atomic -rc -y anitareader

# end
