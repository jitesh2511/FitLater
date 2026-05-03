"""
Session state container.

Simple holder for session-scoped state: the loaded DataFrame and
associated file path.
"""


class Session:
    def __init__(self):
        self.df = None
        self.file_path = None