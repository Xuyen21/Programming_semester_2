
# Dashboard: dblp Dataset

This is a Dashboard built for easy data visualization of the
DBLP dataset. It uses a Postgres database to access the required data promptly.

## Installation

To use the Dashboard, make sure to install all the modules listed in `requirements.txt`.

## Database

The `dblp.xml` file has been converted to a SQL database using a self-made script. The different Tables of the Database can be seen under `docs/Database.md`.

The file has been converted using `app/xml_parser.py`. Do not run this script, as it takes multiple hours to finish inserting all the tables into the database.

## Elements

The file `docs/elements.json` provides an overview of the elements per category of the dataset.

## Version control using git

Changes are versioned with git and each new feature is introduced through a GitHub pull request.

## Environment

To connect to the Postgres Database, you need a few environment variables.

```env
DATABASE_NAME = The name of your database
POSTGRES_USER = The username of your database
POSTGRES_PASSWORD = The password for the specified user
```

When using VSCode to run the Dashboard, you also need the
following environment variables.

```env
VSCODE = "True"
WORKSPACE_FOLDER=Your path to the app folder
PYTHONPATH=./app
```

## Run the Dashboard

To start the Dashboard, just run `dashboard.py`.

When running under VSCODE make sure you run it from within the `app` folder.