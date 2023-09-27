test:
	pytest tests/

lint:
	black src/

update_submodule:
	git submodule update --remote
