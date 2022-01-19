class GithubPddScan(Exception):
    def __init__(self, message="Generic GithubPddScan exception"):
        self.message = message
        super().__init__(self.message)


class ResourceNotFound(GithubPddScan):
    def __init__(self, repo, filename, branch, message="Resource not found"):
        self.repo = repo
        self.filename = filename
        self.branch = branch
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.repo.full_name} (branch: {self.branch}: {self.message}"
