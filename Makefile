frontend:
	uvicorn front.app:app --reload --host 0.0.0.0 --port 9000
backend:
	uvicorn api.app:app --reload --host 0.0.0.0 --port 8000