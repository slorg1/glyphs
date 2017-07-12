from __future__ import unicode_literals
import six


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

    __slots__ = tuple()
