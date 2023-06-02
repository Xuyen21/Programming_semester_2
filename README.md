
# Dashboard: dblp Dataset

This is a Dashboard built for easy data visualization of the
DBLP dataset. It uses a Postgres database to access the required data promptly.

## Installation

To install the latest version of the Dashboard please download the latest Release on GitHub.
After downloading please install the required Modules listed in `requirements.txt`. When using pip use the following command.

```zsh
pip3 install -r requirements.txt
```

The last step is to define all the required environment variables.
If you use a `.env` file, place it in the same directory as the app folder.

## Database

The `dblp.xml` file has been converted to a SQL database using a self-made xml parser. The different Tables of the Database can be seen under `docs/Database.md`.

The file has been converted using `app/xml_parser.py`. Do not run this script, as it takes multiple hours to finish inserting all the tables into the database.

## Elements

The file `docs/elements.json` provides an overview of the elements per category of the dataset.

## Environment

To connect to the Postgres Database, you need a few environment variables.

```env
DATABASE_NAME = The name of your database
POSTGRES_USER = The username of your database (Default: postgres)
POSTGRES_PASSWORD = The password for the specified user
```

When using VSCode to run the Dashboard, you also need the
following environment variables.

```env
VSCODE = "True"
WORKSPACE_FOLDER = Your path to the app folder
PYTHONPATH = ./app
```

## Run the Dashboard

To start the Dashboard, just run `dashboard.py`.

When running under VSCODE make sure you run it from within the `app` folder.

## Version control using git

Changes are versioned with git and each new feature is introduced through a GitHub pull request.

## Known issues

When switching tabs or filters before the chart is properly loaded, it is possible to run into a state, where an empty chart gets displayed. In this case, try to change the filter. If that doesn't help please delete the content of the `.cache` folder and restart the dashboard.
