from __future__ import unicode_literals

import six

from glyphs.helpers.ImmutableType import ImmutableType


class ImmutableObject(six.with_metaclass(ImmutableType)):
    """
        Abstract class making any implementation and instance of this class immutable.

        i.e. no instance and class attributes will able to be set.
    """

    def __setattr__(self, name, value):
        assert False, "No sets allowed for instances of %(class_name)s" % {"class_name" :self.__class__.__name__}

    __slots__ = tuple()
