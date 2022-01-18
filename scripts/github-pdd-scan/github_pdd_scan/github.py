import logging
import re
import urllib
import requests


class GitHub:
    def __init__(self, github_token, org_name, logger=None) -> None:
        self.github_token = github_token
        self.org_name = org_name
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger()
        self.github_api_headers = {"accept": "application/vnd.github.v3+json"}
        self.auth_header = {"Authorization": f"token {github_token}"}

    def get_repos(self, include_pattern=None, exclude_pattern=None, archived=False):
        self.logger.debug("Start of function")

        inpat_re = re.compile(include_pattern) if include_pattern else None
        expat_re = re.compile(exclude_pattern) if exclude_pattern else None

        url = "https://api.github.com/orgs/{}/repos".format(
            urllib.parse.quote_plus(self.org_name)
        )
        github_api_headers = self.github_api_headers

        while True:
            self.logger.debug(
                f"Calling {url} with {github_api_headers=} plus auth token"
            )
            r = requests.get(url, headers=github_api_headers.update(self.auth_header))
            r.raise_for_status()
            repo_json = r.json()
            for repo in repo_json:
                if not archived and repo["archived"]:
                    continue
                if inpat_re and not inpat_re.search(repo["name"]):
                    continue
                if expat_re and expat_re.search(repo["name"]):
                    continue
                yield repo["name"]
            if "next" in r.links and "url" in r.links["next"]:
                url = r.links["next"]["url"]
            else:
                break

        self.logger.debug("End of function")
        return None
