stop:
	docker compose down

run:
	docker compose up --build web db

restart: stop run

db.shell:
	docker exec -it db sh -c "psql -Upostgres"

db.seed: build.web  ## Send a message to RabbitMQ
	docker exec -it web sh -c "uv run python -m scripts.db_seed"

db.clear: build.web  ## Send a message to RabbitMQ
	docker exec -it web sh -c "uv run python -m scripts.db_seed --clear"

run.test_app:
	docker compose up -d test_web

test: run.test_app
	docker exec -it test_web sh -c "uv run pytest . -vv"

test.coverage: run.test_app
	docker exec -it test_web sh -c "uv run pytest --cov-report term --cov=app . -vv"

build.web:
	docker compose build web

lint: build.web
	docker run --rm homeproject-web sh -c "uv run black --color . && uv run ruff check --fix && uv run mypy . && uv run codespell --enable-colors /app && uv run refurb ."