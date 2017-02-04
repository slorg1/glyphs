from __future__ import unicode_literals

class ImmutableType(type):
    """
        Abstract type making any implementing class immutable.

        i.e. no static attributes will able to be set.
    """

    def __setattr__(cls, name, value):
        assert False, "No sets allowed for %(class_name)s" % {"class_name" :cls.__name__}
