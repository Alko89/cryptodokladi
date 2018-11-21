# cryptodokladi

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/912fccdd4f654710a2695789cee7c1d0)](https://app.codacy.com/app/Alko89/cryptodokladi?utm_source=github.com&utm_medium=referral&utm_content=Alko89/cryptodokladi&utm_campaign=Badge_Grade_Dashboard)

## Getting Started

- Change directory into your newly created project.

    `cd cryptodokladi`

- Create a Python virtual environment.

    `python3 -m venv env`

- Upgrade packaging tools.

    `env/bin/pip install --upgrade pip setuptools`

- Install the project in editable mode with its testing requirements.

    `env/bin/pip install -e ".[testing]"`

- Configure the database.

    `env/bin/initialize_cryptodokladi_db development.ini`

- Run your project's tests.

    `env/bin/pytest`

- Install npm packages and build frontend

    `npm install & npm run build`

- Run your project.

    `make run`
