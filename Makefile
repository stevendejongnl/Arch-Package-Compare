image:
	docker buildx build \
		--tag packages \
		--load \
		-f Dockerfile .

mypy:
	docker run -v ${CURDIR}:/app packages mypy --config-file /app/mypy.ini /app

flake:
	docker run -v ${CURDIR}:/app packages flake8 .

mypy-flake: mypy flake
