.PHONY: backend frontend test up down
backend:
	cd backend && uvicorn app.main:app --reload
frontend:
	cd frontend && npm run dev
test:
	cd backend && python -m pytest ../tests
up:
	docker compose up --build
down:
	docker compose down
