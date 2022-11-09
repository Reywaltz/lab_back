lint:
	flakeheaven lint
	mypy .

isort:
	isort . --recursive

mypy:
	mypy .

dev-server:
	uvicorn src:app --reload --debug
