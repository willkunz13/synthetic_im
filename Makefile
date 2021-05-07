.ONESHELL:
SHELL := /bin/bash
SRC = $(wildcard lib/*.ipynb)

all: synthetic_im docs

synthetic_im: $(SRC)
	nbdev_build_lib
	touch synthetic_im

sync:
	nbdev_update_lib

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi conda_release
	nbdev_bump_version

conda_release:
	fastrelease_conda_package

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist