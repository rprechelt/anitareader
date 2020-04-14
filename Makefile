##
# anitareader
#
# @file
# @version 0.0.1

# our testing targets
.PHONY: tests flake black

tests:
	python -m pytest --cov=anitareader tests

flake:
	python -m flake8 anitareader

black:
	python -m black -t py37 anitareader tests

# end
