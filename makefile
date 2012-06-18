validate:
	travis-lint
	tox

clean:
	rm -rf dist
	rm MANIFEST