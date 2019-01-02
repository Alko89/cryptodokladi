# cryptodokladi

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/912fccdd4f654710a2695789cee7c1d0)](https://app.codacy.com/app/Alko89/cryptodokladi?utm_source=github.com&utm_medium=referral&utm_content=Alko89/cryptodokladi&utm_campaign=Badge_Grade_Dashboard)

CryptoDokladi is a staking pool (currently only supporting PIVX for staking) with a simple UI for users to track their balances.

## Getting Started

- Change directory into your newly created project.

    `cd cryptodokladi`

- Create a Python virtual environment.

    `python3 -m venv env`

- Install dependencies with pip and npm using the Makefile.

    `make install`

- Configure the database.

    `alembic upgrade head`

- Run your project's tests.

    `make test`

- Run your project in development.

    `make run`
