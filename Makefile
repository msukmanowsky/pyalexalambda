.PHONY: docs

docs:
	rm -r docs; cd docs-source && make html && cp -r _build/html ../docs && cd .. && touch docs/.nojekyll && echo "Sphinx docs are in docs/"
