check:
	ruff check .

lint:
	ruff check --fix .
	ruff format .

bash:
	docker compose exec flask bash

shell:
	docker compose exec flask shell