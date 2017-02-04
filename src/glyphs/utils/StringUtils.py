from __future__ import unicode_literals


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
            @postcondition: return is None or isinstance(return, unicode)
        """
        return value if value is None else unicode(value)

    __slots__ = tuple()
