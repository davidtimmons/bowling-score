"""This module contains general helper functions for use with other modules."""


def read_only(fn):
    """Decorator used to make a class function read_only.

    Args:
        fn: Class function used to return a read_only value.

    Returns:
        Function that returns a read_only value.
    """

    def fset(self, value):
        raise TypeError

    def fget(self):
        return fn(self)

    return property(fget, fset)


if __name__ == '__main__':
    pass
