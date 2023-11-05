install_test:
	pip install -r tests/requirements.txt

test:
	pytest tests/


install_tools:
	pip install black  setuptools pylama pytest

lint:
	black . --exclude 'api/pdf_parser/*'
	pylama .

update_submodule:
	git submodule update --remote
