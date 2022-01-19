# github-pdd-scan

Scan the folio-org GitHub organization for active repos containing PERSONAL_DATA_DISCLOSURE.md documents.

## Installation

    PIPENV_VENV_IN_PROJECT=1 pipenv install

## Usage

Be sure to `pipenv shell` to get into the program's environment prior to running commands.

    github-ppd-scan --github-token GITHUB_PERSONAL_ACCESS_TOKEN [-v|-d] inventory-ppd [--include REGEX] [--exclude REGEX] [--archived]

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment using `pipenv`:

    PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
    pipenv shell
    pipenv -e .

Or without `pipenv`, something like this:

    cd github-pdd-scan
    python -m venv venv
    source venv/bin/activate

Now install the dependencies:

    pip install -e '.[dev]'

