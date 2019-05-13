from __future__ import unicode_literals

import six
from builtins import None


class StringUtils(object):
    """
        Utility class for handling strings.
    """

    @staticmethod
    def to_unicode(value):
        """
            Returns the string representation of the given L{value} if it is not C{None}. Otherwise,
            returns C{None}.

            @postcondition: (value is None) == (return is None)
            @postcondition: return is None or isinstance(return, six.text_type)
        """

        return value if value is None else six.text_type(value)

    @staticmethod
    def to_unicode_not_empty(value):
        """
            Returns the string representation of the given L{value} if it is not C{None} and not empty. Otherwise,
            returns C{None}

            @postcondition: returns is None or isinstance(returns, six.text_type)
        """

        return_value = StringUtils.to_unicode(value)

        if not return_value:
            return None

        return return_value

    @staticmethod
    def to_unicode_not_none(value):
        """
            Returns the string representation of the given L{value} if it is not C{None}.

            @rtype: six.text_type

            @raise ValueError: raises a value error if the given L{value} is {None}
        """

        if value is None:
            raise ValueError()

        return six.text_type(value)

    @staticmethod
    def to_unicode_not_empty_not_none(value):
        """
            Returns the string representation of the given L{value} if it is not C{None} and not empty.

            @rtype: six.text_type

            @raise ValueError: raises a value error if the given L{value} is {None} or an empty string
        """

        return_value = StringUtils.to_unicode_not_empty(value)

        if not return_value:
            raise ValueError()

        return return_value

    __slots__ = tuple()
