"""helpers.py

Provides general helper functions for use with other modules.
"""


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


class restrict_bounds(object):
    """Restrict the numeric bounds of a function argument.

    Checks the first two arguments to a function and tests the first one that may be
    a number. Pass the remaining arguments through to the function. This decorator can
    work with class functions or plain functions. While this decorator currently bounds
    only a single argument, it can be extended to restrict the bounds of multiple arguments.

    Args:
        left_bound: Integer representing the left bound, inclusive, or a function that
            returns an integer saved as an instance variable.
        right_bound: Integer representing the right bound, inclusive, or a function that
            returns an integer saved as an instance variable.

    Example:
        left_bound  = 0
        right_bound = 10
        right_bound = lambda self: self.__num_pins

    Raises:
        ValueError when the argument is outside the bounds.

    Returns:
        Decorated function.
    """

    def __init__(self, left_bound, right_bound):
        """Initialize the bounds."""
        self.left_bound = left_bound
        self.right_bound = right_bound


    def __call__(self, fn):
        """Wrap the function with a bounds check."""

        # Keep a reference to the decorator object.
        that = self

        def wrapped_fn(*args, **kwargs):

            # Get the first or second arg, depending on whether this is a class function.
            args = [*args]
            arg_1 = arg = args[0] ## Maybe class object?
            arg_2 = None
            self = None

            if len(args) > 1:
                arg_2 = args[1]

            # Check if the first argument is class object.
            if hasattr(arg_1, '__dict__'):
                self = arg_1
                arg = arg_2

            # Get the bounds; call the bounds functions if they exist.
            left_bound = that.left_bound
            if callable(left_bound):
                left_bound = left_bound(self)

            right_bound = that.right_bound
            if callable(right_bound):
                right_bound = right_bound(self)

            # Check bounds.
            if that.is_number(arg) and left_bound <= arg and right_bound >= arg:
                return fn(*args, **kwargs)

            raise ValueError('The argument should be a number between {left} and {right}!' \
                .format(left=repr(left_bound), right=repr(right_bound)))

        return wrapped_fn


    def is_number(self, maybe_number):
        """Checks an unknown argument to see if it is a number (int, float, or complex).

        Args:
            maybe_number: Unknown argument to test.

        Returns:
            Boolean indicating whether the argument is a number or not.
        """
        try:
            complex(maybe_number)
        except ValueError:
            return False
        except TypeError:
            return False

        return True


if __name__ == '__main__':
    pass
