.PHONY: docs

docs:
	cd docs-source && make html && cp -r _build/html ../docs && cd .. && echo "Sphinx docs are in docs/"
