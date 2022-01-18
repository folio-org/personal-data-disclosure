import sys
import logging
import click

from .github import GitHub


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
            "--archived",
            "archived",
            help="include archived repositories",
            flag_value=False,
        ),
        click.option(
            "--no-archived",
            "archived",
            help="don't Include archived repositories (default)",
            flag_value=False,
            default=True,
            show_default=True,
        ),
    ):
        fn = decorator(fn)
    return fn


@click.group()
@click.version_option()
@click.argument("github_token")
@click.pass_context
def cli(ctx, github_token):
    "Scan GitHub repositories for PERSONAL_DATA_DISCLOSURE documents"
    logger = logging.getLogger(sys.argv[0])
    FORMAT = "%(asctime)s - %(levelname)s - %(module)s@%(lineno)s - %(message)s"
    logging.basicConfig(format=FORMAT)

    ctx.obj = Config(github_token, logger)


@cli.command(name="get-repos")
@include_exclude_options
@click.pass_context
def get_repos(ctx, include, exclude, archived):
    github = GitHub(ctx.obj.github_token, "folio-org", logger=ctx.obj.logger)
    for repo in github.get_repos(
        include_pattern=include, exclude_pattern=exclude, archived=archived
    ):
        click.echo(repo)
