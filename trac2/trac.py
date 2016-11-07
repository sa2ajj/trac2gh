"""
interface to trac
"""
from __future__ import absolute_import

from collections import defaultdict

from trac.env import Environment
from trac.ticket.model import Ticket
from trac.ticket.query import Query

from trac2.trac2md import format_text


class TracTicket(object):
    """
    internal representation of a track ticket
    """
    def __init__(self, adaptor, ticket):
        self._adaptor = adaptor
        self._ticket = ticket

    def as_dict(self):
        """
        produce ticket representation as a dictionary
        """
        tempo = self._ticket.values.copy()

        contributors = defaultdict(list)

        reporter = tempo.pop('reporter', None)
        if reporter:
            contributors[self._adaptor.user(reporter)].append('reporter')

        owner = tempo.pop('owner', None)
        if owner:
            contributors[self._adaptor.user(owner)].append('owner')

        for item in self._adaptor.normalise_list(', '.join(tempo.pop('cc',
                                                                     list()))):
            contributors[item].append('watcher')

        for _, author, _, _, _, _ in self._ticket.get_changelog():
            contributors[self._adaptor.user(author)].append('commenter')

        tempo['contributors'] = dict(contributors)
        tempo['description'] = format_text(tempo['description'])
        tempo['id'] = self._ticket.id
        tempo['url'] = self._adaptor.env.abs_href.ticket(self._ticket.id)

        return tempo

    def mark_exported(self, issue, url):
        """
        mark the ticket as exported
        """


class TracAdaptor(object):
    """
    interface b/w a trac instance and the converter
    """
    def __init__(self, config, dry_run=False):
        self._dry_run = dry_run

        self._milestones = config['milestones']

        self._env = Environment(config['env'])
        self._users = dict({
            username: email for
            username, _, email in self._env.get_known_users()
        })

    @property
    def env(self):
        """
        Trac environment
        """
        return self._env

    def ticket(self, data):
        """
        create a wrapper over a Trac ticket
        """
        return TracTicket(self, Ticket(self._env, data['id']))

    def normalise_list(self, user_list):
        """
        normalise user list
        """
        return [self.user(user) for user in user_list.replace(',', ' ').split()]

    def user(self, user):
        """
        normalise user's email
        """
        return self._users.get(user, user)

    @staticmethod
    def trac2md(text):
        """
        somewhat convert trac markup to markdown one
        """

    def get_tickets(self):
        """
        yield all the tickets per self._env and self._milestones
        """
        query = [
            'status!=closed'
        ]

        if self._milestones:
            query.append('milestone={}'.format(
                '|'.join(mstone for mstone in self._milestones)))

        for ticket in Query.from_string(self._env, '&'.join(query)).execute():
            yield self.ticket(ticket)
