"""
interface to trac
"""
class TracAdapter(object):
    def __init__(self, env, milestones):
        self._env = env
        self._milestones = milestones

    def get_tickets(self):
        """
        yield all the tickets available in the 'env'
        """
        raise NotImplementedError
