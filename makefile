install_test:
	pip install -r tests/requirements.txt

test:
	pytest tests/

lint:
	black api/

update_submodule:
	git submodule update --remote
