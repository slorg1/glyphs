from __future__ import unicode_literals

from glyphs.ro.ROGlyph import ROGlyph
from glyphs.utils.StringUtils import StringUtils


class RWGlyph(ROGlyph):
    """
        Read/write glyph is designed to read data from an object and write data back.
    """

    def __init__(self, r_path, w_path, r_types=None, w_types=None,
                 r_translation_function=None,
                 w_translation_function=StringUtils.to_unicode,
                 r_default_value=None,
                 w_allow_none=False,
                 ):
        """
            Initializer for a R/W glyph instance.

            @param w_path: The "path" pointing to where the data needs to be written.
            For multilevel keys (nest level):
            - if the path is a unicode, use L{a name space separator<glyphs.api.ROGlyph.ROGlyph.NAME_SPACE_SEPARATOR>}
            between the various level of keys.
            - if the path is a collection, each level is a unicode in the collection.
            @type w_path: unicode or collections.Sequence
            @param w_types: (Optional) A string describing the type of data expected to be found once the data
            is written. For each matching level in L{w_path}, a key-value pair may be specified, not all
            levels are required to have a type defined.
            - if L{w_types} is a unicode, use L{a name space separator<glyphs.api.ROGlyph.ROGlyph.NAME_SPACE_SEPARATOR>}
            between the various level of types. To omit a level of type, do not specify a key-value pair.
            - if L{w_types} is a collection, each level of types is a unicode in the collection. To omit a
            level of type, place C{None} at the skipped level.

            The level of types are key-value pairs. The key defines where the type information can be found at
            a given level in the source. The values specifies the type expected. The key and value separator
            <glyphs.api.ROGlyph.ROGlyph.KEY_VALUE_SEPARATOR>}.
            There is no need to specify every level of type to match L{w_path},
            as any long-tail levels that are not specified will be interpreted as having no key-value
            pairs.
            @param w_translation_function: function used to translate the data to be written at L{w_path}
            to any target format.
            This is meant to be a very simple function for pure translate / transtyping. No intelligence here.
            If C{None}, then no translation is needed and the data should be passed through.
            @param w_allow_none: C{True} if the object supports a C{None} value (when written into). Otherwise,
            C{False}.

            @precondition: isinstance(w_path, unicode) or all(isinstance(u, unicode) for u in w_path)
            @precondition: len(w_path) > 0
            @precondition: w_types is None or isinstance(w_types, (unicode, tuple))
            @precondition: w_types is None or len(w_types) > 0
            @precondition: w_types is None or isinstance(w_types, tuple) or (
                                                                                     (
                                                                                     isinstance(w_path, unicode)
                                                                                     and w_types.count(ROGlyph.NAME_SPACE_SEPARATOR) <= w_path.count(ROGlyph.NAME_SPACE_SEPARATOR)
                                                                                     )
                                                                                     or w_types.count(ROGlyph.NAME_SPACE_SEPARATOR) <= len(w_path)
                                                                                     )
            @precondition: w_types is None or isinstance(w_types, unicode) or (
                                                                                     (
                                                                                     isinstance(w_path, unicode)
                                                                                     and len(w_types) <= w_path.count(ROGlyph.NAME_SPACE_SEPARATOR)
                                                                                     )
                                                                                     or len(w_types) <= len(w_path)
                                                                                     )
            @precondition: w_types is None or len(w_types) > 0
            @precondition: w_translation_function is None or callable(w_translation_function)

            @see: glyphs.api.ROGlyph.ROGlyph.__init__
        """
        super(RWGlyph, self).__init__(
                                      r_path,
                                      r_types,
                                      r_translation_function,
                                      r_default_value,
                                      )

        self.__dict__["__w_translation_function"] = w_translation_function
        self.__dict__["__w_path_type"] = self._generate_path_type_paired_sequence(w_path, w_types,)
        self.__dict__["__w_allow_none"] = w_allow_none

    @property
    def iter_w_path_type(self):
        """
            Returns a new iterator through the configured sequence of triplet of the sub path, their matching
            types as a pair and a boolean expressing whether they are the last triplet in the sequence.

            The iterator makes up a typed path to write data into an object.

            @rtype: collections.Iterable

            @postcondition: next(return, None) is not None
            @postcondition: all(
                                (
                                    isinstance(x, tuple)
                                    and len(x) == 3
                                    and isinstance(x[0], bool)
                                    and isinstance(x[1], unicode) and len(x[1]) > 0
                                    and (
                                        x[2] is None
                                        or (
                                            isinstance(x[2], tuple) and len(x[2]) == 2
                                            and all(isinstance(v) for v in x[2])
                                           )
                                        )
                                )
                                for x in return
                                )
        """
        return iter(self.__dict__["__w_path_type"])

    @property
    def w_translation_function(self):
        """
            Returns a function used to translate a value to the format expected in the object.

            Note: this is meant to be a very simple function for pure translate / transtyping. No
            intelligence here.

            If C{None}, then no translation is needed and the data should be passed through.

            @postcondition: return is None or callable(return)

        """
        return self.__dict__["__w_translation_function"]

    @property
    def w_allow_none(self):
        """
            Returns C{True} if the object supports s C{None} value (when written into). Otherwise, returns
            C{False}.

            @rtype: bool
        """
        return self.__dict__["__w_allow_none"]
