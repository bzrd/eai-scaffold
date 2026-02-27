.PHONY: lint format test test-unit test-integration build-all build clean help

PYTHON := python3.12
REGISTRY := registry.intern
COMPONENT ?=

## help: Display this help message
help:
	@echo "EAI System – Verfügbare Make-Targets:"
	@echo ""
	@sed -n 's/^## //p' $(MAKEFILE_LIST) | column -t -s ':' | sed -e 's/^/  /'

## lint: Ruff check + mypy über das gesamte Repo
lint:
	ruff check libs/ transformers/ base-containers/ tests/
	mypy libs/ transformers/ base-containers/ --config-file pyproject.toml

## format: Ruff format über das gesamte Repo
format:
	ruff format libs/ transformers/ base-containers/ tests/

## test: Alle Unit-Tests ausführen
test: test-unit

## test-unit: Nur Unit-Tests (kein laufendes System erforderlich)
test-unit:
	$(PYTHON) -m pytest -m "unit or not integration" --tb=short libs/ transformers/ base-containers/

## test-integration: Nur Integrationstests (laufende Dev-Umgebung erforderlich)
test-integration:
	@echo "Warnung: Integrationstests benötigen eine laufende Dev-Umgebung."
	@echo "Stelle sicher dass DS_API_URL und DS_API_TOKEN gesetzt sind."
	$(PYTHON) -m pytest -m integration tests/integration/ --tb=short -v

## build-all: Alle Container-Images bauen
build-all:
	@echo "Baue alle Transformer..."
	@for dir in transformers/*/; do \
		name=$$(basename $$dir); \
		if [ "$$name" != "_template" ]; then \
			docker build -f docker/Dockerfile.transformer \
				--build-arg COMPONENT=$$name \
				-t $(REGISTRY)/transformer-$$name:dev .; \
		fi \
	done
	@echo "Baue alle Base-Container..."
	@for dir in base-containers/*/; do \
		name=$$(basename $$dir); \
		if [ "$$name" != "_template" ]; then \
			if [ "$$name" = "http-trigger" ]; then \
				docker build -f docker/Dockerfile.http-trigger \
					-t $(REGISTRY)/base-$$name:dev .; \
			else \
				docker build -f docker/Dockerfile.base \
					--build-arg COMPONENT=$$name \
					-t $(REGISTRY)/base-$$name:dev .; \
			fi \
		fi \
	done

## build COMPONENT=<name>: Einzelnes Container-Image bauen (z.B. make build COMPONENT=transformer-ingest)
build:
	@if [ -z "$(COMPONENT)" ]; then \
		echo "Fehler: COMPONENT nicht gesetzt. Beispiel: make build COMPONENT=transformer-ingest"; \
		exit 1; \
	fi
	@type=$$(echo $(COMPONENT) | cut -d- -f1); \
	name=$$(echo $(COMPONENT) | cut -d- -f2-); \
	if [ "$$type" = "transformer" ]; then \
		docker build -f docker/Dockerfile.transformer \
			--build-arg COMPONENT=$$name \
			-t $(REGISTRY)/$(COMPONENT):dev .; \
	elif [ "$$type" = "base" ]; then \
		if [ "$$name" = "http-trigger" ]; then \
			docker build -f docker/Dockerfile.http-trigger \
				-t $(REGISTRY)/$(COMPONENT):dev .; \
		else \
			docker build -f docker/Dockerfile.base \
				--build-arg COMPONENT=$$name \
				-t $(REGISTRY)/$(COMPONENT):dev .; \
		fi \
	else \
		echo "Unbekannter Typ: $$type. Erwartet: transformer oder base"; \
		exit 1; \
	fi

## clean: Build-Artefakte aufräumen
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name dist -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name build -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
