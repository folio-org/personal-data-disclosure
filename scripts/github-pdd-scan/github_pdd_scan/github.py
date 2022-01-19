import logging
import re
import collections
import urllib
import requests
from .exceptions import *

GithubRepo = collections.namedtuple(
    "GithubRepo",
    [
        "name",
        "full_name",
        "api_url",
        "default_branch",
        "archived",
    ],
)

PddDocument = collections.namedtuple(
    "PddDocument",
    [
        "repo",
        "raw_url",
        "last_modified",
    ],
)


class GitHub:
    def __init__(self, github_token, org_name, logger=None) -> None:
        self.github_token = github_token
        self.org_name = org_name
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger()
        self.github_api_headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {github_token}",
        }

    def get_repos(self, include_pattern=None, exclude_pattern=None, archived=False):
        self.logger.debug("Start of function")

        inpat_re = re.compile(include_pattern) if include_pattern else None
        expat_re = re.compile(exclude_pattern) if exclude_pattern else None

        url = "https://api.github.com/orgs/{}/repos?per_page=100".format(
            urllib.parse.quote_plus(self.org_name)
        )
        github_api_headers = self.github_api_headers

        while True:
            self.logger.info(f"Calling {url} with {github_api_headers=}")
            r = requests.get(url, headers=github_api_headers)
            r.raise_for_status()
            repo_json = r.json()
            for repo in repo_json:
                if not archived and repo["archived"]:
                    continue
                if inpat_re and not inpat_re.search(repo["name"]):
                    continue
                if expat_re and expat_re.search(repo["name"]):
                    continue
                yield GithubRepo(
                    repo["name"],
                    repo["full_name"],
                    repo["url"],
                    repo["default_branch"],
                    repo["archived"],
                )
            if "next" in r.links and "url" in r.links["next"]:
                url = r.links["next"]["url"]
            else:
                break

        self.logger.debug("End of function")
        return None

    def get_file_metadata(self, repo, filename, branch="main"):
        self.logger.debug("Start of function")
        github_api_headers = self.github_api_headers

        content_url = (
            f"{repo.api_url}/contents/{urllib.parse.quote_plus(filename)}?ref={branch}"
        )
        self.logger.info(f"Calling {content_url} with {github_api_headers=}")
        r_content = requests.get(content_url, headers=github_api_headers)
        if r_content.status_code == requests.codes.NOT_FOUND:
            raise ResourceNotFound(repo, filename, branch)
        content_dict = r_content.json()

        commit_url = f"{repo.api_url}/commits?path={urllib.parse.quote_plus(filename)}&page=1&per_page=1&sha={branch}"
        self.logger.info(f"Calling {commit_url} with {github_api_headers=}")
        r_commit = requests.get(commit_url, headers=github_api_headers)
        r_commit.raise_for_status()
        commit_dict = r_commit.json()

        pdd = PddDocument(
            repo,
            content_dict["download_url"],
            commit_dict[0]["commit"]["committer"]["date"],
        )
        return pdd
