"""
interface to GitHub
"""
from pprint import pprint

from github3 import GitHub


class GitHubAdaptor(object):
    """
    thin wrapper over github3 with the purpose of importin [trac] tickets
    """
    def __init__(self, config, dry_run=False):
        self._dry_run = dry_run
        self._mapping = config['mapping']

        self._gh = GitHub(token=config['token'])

        # Everything is done via _repo
        self._repo = self._gh.repository(config['owner'], config['repository'])

        # get current set of available milestones
        self._milestones = dict({
            milestone.title: milestone.number
            for milestone in self._repo.milestones()
        })

        self._users = dict()

    def ensure_milestone(self, name):
        """
        check if the given milestone is known already and if it's not create it
        """
        num = self._milestones.get(name, None)

        if num is None:
            milestone = self._repo.create_milestone(name)

            num = self._milestones[name] = milestone.number

        return num

    def get_user(self, email):
        """
        transform the given e-mail to a github username

        cache results
        take into account provided mapping
        """
        user = self._users.get(email)
        if user is None:
            mapped = self._users.get(email, email)
            user = None # magic
            self._users[email] = user

        return user

    def create_issue(self, issue):
        """
        create an issue in the given project
        """
        pprint(issue)

        # stub
        return None, None
