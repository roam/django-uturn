validate:
	travis-lint
	tox

clean:
	rm -rf dist
	rm MANIFEST

sdist:
	python setup.py sdist
	python setup.py bdist_wheel

dryrun:
	rm -rf venv-sdist
	virtualenv venv-sdist
	./venv-sdist/bin/pip install -f dist
	rm -rf venv-wheel
	virtualenv venv-wheel
	./venv-wheel/bin/pip install --use-wheel --find-links dist django_uturn
