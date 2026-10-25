PYTHON ?= python3

.PHONY: all check test-cli generate build install preview variant validate clean

all: check test-cli build validate preview

check:
	@command -v ctgen >/dev/null || { echo "missing ctgen: pip install clickgen"; exit 1; }
	@command -v rsvg-convert >/dev/null || { echo "missing rsvg-convert: install librsvg"; exit 1; }
	@$(PYTHON) -c "import PIL" || { echo "missing Pillow: pip install Pillow"; exit 1; }
	@$(PYTHON) -m compileall -q cli

test-cli:
	$(PYTHON) -m unittest discover -s cli/tests -v

generate:
	$(PYTHON) scripts/generate.py

build: check generate
	$(PYTHON) scripts/build.py

install: check generate
	$(PYTHON) scripts/build.py --install

preview: check build
	$(PYTHON) scripts/preview.py

variant:
	$(PYTHON) cli/cursors-cli --spec $(or $(SPEC),cli/examples/cursor-spec.json) --out-dir $(or $(OUT),build/variants) $(if $(SIZES),--sizes $(SIZES),)

validate:
	$(PYTHON) scripts/validate.py

clean:
	rm -rf build preview
