"""This module contains general helper functions for use with other modules."""


def read_only(fn):
    """Decorator used to make a class function read only.

    Args:
        fn: Class function used to return a read only value.

    Raises:
        TypeError if the function argument enounters a "set" operation.

    Returns:
        Function that returns a read only value.
    """

    def fset(self, value):
        raise TypeError('This is a read only value!')

    def fget(self):
        return fn(self)

    return property(fget, fset)


if __name__ == '__main__':
    pass
