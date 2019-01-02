#Make sure you're working on a virtual environment
venv:
	python3 -m venv env

# Initializes virtual environment with basic requirements.
prod:
	source env/bin/activate; \
	pip install -r requirements.txt; \
	npm install --production \

# Installs development dependencies.
install:
	source env/bin/activate; \
	pip3 install --upgrade pip setuptools; \
	pip3 install -r requirements.txt; \
	npm install; \
	npm run build; \
	python3 setup.py develop; \

# runs tests for your project
test:
	source env/bin/activate; \
	pytest; \

# Runs development server.
# This step depends on `make dev`, however dependency is excluded to speed up dev server startup.
run:
	source env/bin/activate; \
	npm run serve & pserve development.ini --reload

# Cleans up folder by removing node modules and generated files.
clean:
	rm -rf node_modules; \
	rm -rf pyramidVue/static/dist; \
