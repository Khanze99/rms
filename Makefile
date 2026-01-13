local:
	python admin/manage.py runserver
migrate:
	python admin/manage.py makemigrations && python admin/manage.py migrate
sw-rm:
	docker stack rm rms
sw-run:
	docker stack deploy -c docker-swarm.yml rms
secrets:
	docker secret ls
build:
	docker build . -t rms:0.0.5
ls:
	docker service ls


