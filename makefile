test:
	pytest tests/

lint:
	black api/

update_submodule:
	git submodule update --remote
