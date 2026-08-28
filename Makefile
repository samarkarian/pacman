install:
	uv sync

run:
	uv run python3 pac-man.py config.json

debug:
	uv run python3 -m pdb pac-man.py config.json

clean:
	rm -rf .mypy_cache
	find . -type d -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} +


lint:
	uv run flake8 . --exclude=.venv
	uv run mypy . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint