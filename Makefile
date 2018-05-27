.PHONY: docs test


help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies using pip"
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  test        run all your tests using py.test"
	@echo "  dev         run development environment"
	@echo "  rename      rename application, usually run once when bootstrapping"

build:
	docker build -t clweb .

rename:
	@read -p "original application name:" oldname; \
	read -p "new application name:" newname; \
	sed -i "s/$$oldname/$$newname/" manage.py; \
	find $$oldname -name '*.py' -print | xargs sed -i "s/$$oldname/$$newname/"; \
	find tests -name '*.py' -print | xargs sed -i "s/$$oldname/$$newname/"; \
	mv $$oldname $$newname

env:
	sudo easy_install pip && \
	pip install virtualenv && \
	virtualenv .env && \
	.env/bin/activate && \
	make deps

deps:
	pip install -r requirements.txt

serve:
	docker run --rm \
	  -v $(pwd):/usr/src/app \
	  -p 5000:5000 \
	  --name clweb \
	  clweb python -u manage.py server

clean:
	python manage.py clean

lint:
	flake8 --exclude=env --exclude=migrations --max-complexity 6 .

test:
	export BOILERPLATE_ENV=test && \
	python manage.py db migrate && \
	python manage.py db upgrade && \
	py.test tests/test_rbac.py

dev:
	export BOILERPLATE_ENV=dev && \
	python manage.py db migrate && \
	python manage.py db upgrade && \
	python manage.py runserver
