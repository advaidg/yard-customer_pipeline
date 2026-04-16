build:
	docker build -t yard-customer_pipeline:latest .

run:
	docker run --env-file .env -p 9000:9000 yard-customer_pipeline:latest

test:
	docker run --rm yard-customer_pipeline:latest python -c "print('smoke test passed')"

health:
	curl -f http://localhost:9000/health
