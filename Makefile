PYTHON ?= python3

.PHONY: all check generate build install preview validate clean

all: check build validate preview

check:
	@command -v ctgen >/dev/null || { echo "missing ctgen: pip install clickgen"; exit 1; }
	@command -v rsvg-convert >/dev/null || { echo "missing rsvg-convert: install librsvg"; exit 1; }
	@$(PYTHON) -c "import PIL" || { echo "missing Pillow: pip install Pillow"; exit 1; }

generate:
	$(PYTHON) scripts/generate.py

build: check generate
	$(PYTHON) scripts/build.py

install: check generate
	$(PYTHON) scripts/build.py --install

preview: check build
	$(PYTHON) scripts/preview.py

validate:
	$(PYTHON) scripts/validate.py

clean:
	rm -rf build preview
