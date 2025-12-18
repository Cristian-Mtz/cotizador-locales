.PHONY: dev lint format type test seed seed-drop openapi

dev:
	uvicorn app.main:app --reload --port 8000

lint:
	ruff check .

format:
	ruff format .

type:
	mypy .

test:
	pytest -q

seed:
	python -m scripts.seed_locales

seed-drop:
	python -m scripts.seed_locales --drop

openapi:
	curl -s http://127.0.0.1:8000/openapi.json | python -m json.tool > openapi.json
	@echo "Saved openapi.json"
