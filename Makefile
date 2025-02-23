api:
	python manage.py runserver

run_linters:
	isort . --skip migrations && \
	black . --exclude migrations && \
	bandit . --exclude migrations && \
	mypy . --check-untyped-defs --ignore-missing-imports && \
	flake8 . --max-line-length=99 --exclude=.venv,venv,migrations



dc_up:
	docker-compose -f docker-compose-local.yml up -d --build

dc_dn:
	docker-compose -f docker-compose-local.yml down

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate


