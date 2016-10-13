"""
interface to GitHub
"""
class GitHubAdapter(object):
    def __init__(self, project, token):
        self._project = project
        self._token = token

    def create_issue(self, issue):
        """
        create an issue in the given project
        """
        raise NotImplementedError
