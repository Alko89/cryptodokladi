#Make sure you're working on a virtual environment
venv:
	python3 -m venv ../

# Initializes virtual environment with basic requirements.
prod:
	source ../bin/activate; \
	pip install -r requirements.txt; \
	pserve production.ini
	npm install --production

# Installs development dependencies.
dev:
	source ../bin/activate; \
	pip3 install --upgrade pip setuptools; \
	npm install; \
	python3 setup.py develop; \

# runs tests for your project
test:
	source ../bin/activate; \
	pytest; \

# Runs development server.
# This step depends on `make dev`, however dependency is excluded to speed up dev server startup.
run:
	source ../bin/activate; \
	npm run dev & pserve development.ini --reload

# Builds files for distribution which will be placed in /static/dist
build:
	npm run build

# Cleans up folder by removing node modules and generated files.
clean:
	rm -rf node_modules; \
	rm -rf pyramidVue/static/dist; \
