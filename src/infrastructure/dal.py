"""
DAL stands for "Database Access Layer".
currently, this layer includes only the Repository pattern implementation.
"""


class Repository:
    @property
    def session(self):
        raise NotImplementedError

    def get_points(self) -> list[dict]:
        raise NotImplementedError

    def add_point(self, data: dict) -> None:
        raise NotImplementedError
