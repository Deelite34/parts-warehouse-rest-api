check:
	ruff check .

lint:
	ruff check --fix .
	ruff format .

bash:
	docker compose exec flask bash

shell:
	docker compose exec flask flask shell

mbash:
	docker compose exec mongodb bash

msh:
	docker compose exec mongodb mongosh

test:
	docker compose exec flask flask test
