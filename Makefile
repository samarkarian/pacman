install:
	uv sync

run:
	uv run python3 pac-man.py config.json

debug:
	uv run python3 -m pdb pac-man.py config.json

clean:
	rm -rf .mypy_cache build dist
	find . -type d -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} +

lint:
	uv run flake8 . --exclude=.venv,build,dist
	uv run mypy . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

package:
	uv run pyinstaller --noconfirm --clean pac-man.spec
	cp config.json packaging/README.txt packaging/.itch.toml \
	packaging/play.command dist/pac-man/
	uv run python3 -c "import shutil; \
	shutil.make_archive('dist/pac-man', 'zip', 'dist/pac-man')"

.PHONY: install run debug clean lint package
