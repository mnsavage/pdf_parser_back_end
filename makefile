test:
	pytest tests/

lint:
	find . -name "*.py" | xargs black

update_submodule:
	git submodule update --remote
