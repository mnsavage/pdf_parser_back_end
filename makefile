install_test:
	pip install -r tests/requirements.txt

test:
	pytest tests/

lint:
	black .
	pylama .

update_submodule:
	git submodule update --remote
