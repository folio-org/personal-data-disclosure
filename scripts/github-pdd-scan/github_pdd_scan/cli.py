import sys
import re
import logging
import click

from github_pdd_scan.exceptions import ResourceNotFound

from .github import GitHub


class RedactingFormatter(object):
    def __init__(self, orig_formatter, patterns):
        self.orig_formatter = orig_formatter
        self._patterns = patterns
        self._regex_patterns = []
        for p in patterns:
            self._regex_patterns.append(re.compile(p))

    def format(self, record):
        msg = self.orig_formatter.format(record)
        for pattern in self._regex_patterns:
            msg = re.sub(pattern, "REDACTED", msg, count=0)
        return msg

    def __getattr__(self, attr):
        return getattr(self.orig_formatter, attr)


class Config(object):
    def __init__(self, github_token, logger):
        self.github_token = github_token
        self.logger = logger


def include_exclude_options(fn):
    for decorator in (
        click.option(
            "--include",
            "-i",
            help="only include repos matching this regex pattern. Note: exclude is given preference over include.",
            default="stripes-|ui-|mod-",
            show_default=True,
            is_flag=False,
            metavar="RE",
        ),
        click.option(
            "--exclude",
            "-e",
            help="exclude repos matching this regex pattern.",
            metavar="RE",
        ),
        click.option(
            "--archived/--no-archived",
            "archived",
            help="include archived repositories",
            default=False,
            show_default=True,
        ),
    ):
        fn = decorator(fn)
    return fn


@click.group()
@click.version_option()
@click.option(
    "--github-token",
    envvar="GITHUB_TOKEN",
    required=True,
    help="GitHub Personal Access Token",
)
@click.option(
    "-d",
    "--debug",
    "log_level",
    flag_value=logging.DEBUG,
    help="turn on debug messages",
)
@click.option(
    "-v",
    "--verbose",
    "log_level",
    flag_value=logging.INFO,
    help="turn on verbose messages",
)
@click.pass_context
def cli(ctx, github_token, log_level):
    "Scan GitHub repositories for PERSONAL_DATA_DISCLOSURE documents"
    logger = logging.getLogger(sys.argv[0])
    FORMAT = "%(asctime)s - %(levelname)s - %(module)s@%(lineno)s - %(message)s"
    logging.basicConfig(format=FORMAT)
    if log_level:
        logger.setLevel(log_level)
    else:
        logger.setLevel(logging.WARNING)
    for h in logging.root.handlers:
        h.setFormatter(RedactingFormatter(h.formatter, patterns=[r"\bghp_.*?\b"]))

    ctx.obj = Config(github_token, logger)


@cli.command(name="inventory-pdd")
@include_exclude_options
@click.pass_context
def inventory_pdd(ctx, include, exclude, archived):
    github_org = "folio-org"
    github = GitHub(ctx.obj.github_token, github_org, logger=ctx.obj.logger)
    results = dict()
    for repo in github.get_repos(
        include_pattern=include, exclude_pattern=exclude, archived=archived
    ):
        branch = repo.default_branch
        filename = "PERSONAL_DATA_DISCLOSURE.md"
        try:
            pdd = github.get_file_metadata(repo, filename, branch)
        except ResourceNotFound as e:
            results[repo.full_name] = "PDD document not found"
        else:
            results[
                repo.full_name
            ] = f"PDD document last updated {pdd.last_modified}: {pdd.raw_url}"

    row_format = "{:>30} {}"
    for repo in results:
        print(row_format.format(repo, results[repo]))
