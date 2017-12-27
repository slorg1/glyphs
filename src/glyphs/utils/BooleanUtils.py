from __future__ import unicode_literals

from glyphs.utils.StringUtils import StringUtils

from glyphs.backports.lru_cache import lru_cache


class BooleanUtils(object):
    """
        Utility class for handling booleans.
    """

    TRUE_VALUES = frozenset(('true', 't', True,))
    """ Set of values considered to be C{True}."""

    @staticmethod
    @lru_cache(typed=True)
    def to_boolean(value):
        """
            Returns the boolean (from the L{true values<BooleanUtils.TRUE_VALUES>}) representation of the
            given L{value} if it is not C{None}. Otherwise, returns C{None}.

            @postcondition: (value is None) == (return is None)
            @postcondition: return is None or isinstance(return, bool)
        """
        return (value if value is None or isinstance(value, bool) else StringUtils.to_unicode(value).lower()) in BooleanUtils.TRUE_VALUES

    __slots__ = tuple()
