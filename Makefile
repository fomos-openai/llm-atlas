NODE ?= node
PYTHON ?= python3

.PHONY: validate lab-smoke atlas book

validate:
	$(NODE) scripts/validate_structure.mjs
	$(NODE) scripts/validate_content.mjs
	$(NODE) scripts/validate_sources.mjs
	$(NODE) scripts/validate_catalogs.mjs
	$(PYTHON) scripts/validate_labs.py

lab-smoke:
	cd labs && PYTHONPATH=src $(PYTHON) -m unittest discover -s tests

atlas:
	$(NODE) scripts/build_atlas.mjs

book:
	$(PYTHON) scripts/build_book.py

