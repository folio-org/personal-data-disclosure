# github-pdd-scan

Scan the folio-org GitHub organization for active repos containing PERSONAL_DATA_DISCLOSURE.md documents.

## Installation

    PIPENV_VENV_IN_PROJECT=1 pipenv install
    pipenv shell

## Usage

Usage instructions go here.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment using `pipenv`:

    PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
    pipenv shell
    pipenv -e .

Or without `pipenv`, something like this:

    cd github-pdd-scan
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

