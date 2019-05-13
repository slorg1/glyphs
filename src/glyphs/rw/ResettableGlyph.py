from __future__ import unicode_literals

from glyphs.rw.RWGlyph import RWGlyph
from glyphs.utils.StringUtils import StringUtils


class ResettableGlyph(RWGlyph):
    """
        Special read/write glyph is designed to read data from an object and write data back.

        It also has the ability to write a value expressing a "force reset" (when supported) into the object.
    """

    def __init__(self, reset_w_path, reset_value,
                 r_path, w_path=None, r_types=None,
                 w_types=None,
                 reset_w_type=None,
                 r_translation_function=None,
                 w_translation_function=StringUtils.to_unicode,
                 r_default_value=None,
                 w_allow_none=False,
                 ):
        """
            Initializer for a resettable R/W glyph instance.

            @param reset_w_path: The "path" pointing to where the data needs to be written to express a "force
            reset" (when supported).
            For multilevel keys (nest level):
            - if the path is a unicode, use L{a name space separator<glyphs.api.ROGlyph.ROGlyph.NAME_SPACE_SEPARATOR>}
            between the various level of keys.
            - if the path is a collection, each level is a unicode in the collection.
            @type reset_w_path: six.text_type or tuple
            @param reset_w_type: (Optional) A string describing the type of data expected to be found once the data
            is written. For each matching level in L{reset_w_path}, a key-value pair may be specified, not all
            levels are required to have a type defined.
            - if L{reset_w_type} is a unicode, use L{a name space separator<glyphs.api.ROGlyph.ROGlyph.NAME_SPACE_SEPARATOR>}
            between the various level of types. To omit a level of type, do not specify a key-value pair.
            - if L{reset_w_type} is a collection, each level of types is a unicode in the collection. To omit a
            level of type, place C{None} at the skipped level.

            The level of types are key-value pairs. The key defines where the type information can be found at
            a given level in the source. The values specifies the type expected. The key and value separator
            <glyphs.api.ROGlyph.ROGlyph.KEY_VALUE_SEPARATOR>}.
            There is no need to specify every level of type to match L{reset_w_path},
            as any long-tail levels that are not specified will be interpreted as having no key-value
            pairs.


            @param reset_value: The reset value

            @precondition: isinstance(reset_w_path, six.text_type) or all(isinstance(u, six.text_type) for u in reset_w_path)
            @precondition: len(reset_w_path) > 0
            @precondition: reset_w_type is None or isinstance(reset_w_type, (six.text_type, tuple))
            @precondition: reset_w_type is None or len(reset_w_type) > 0
            @precondition: reset_w_type is None or isinstance(reset_w_type, tuple) or (
                                                                                     (
                                                                                     isinstance(reset_w_path, six.text_type)
                                                                                     and reset_w_type.count(ROGlyph.NAME_SPACE_SEPARATOR) <= reset_w_path.count(ROGlyph.NAME_SPACE_SEPARATOR)
                                                                                     )
                                                                                     or reset_w_type.count(ROGlyph.NAME_SPACE_SEPARATOR) <= len(reset_w_path)
                                                                                     )
            @precondition: reset_w_type is None or isinstance(reset_w_type, six.text_type) or (
                                                                                     (
                                                                                     isinstance(reset_w_path, six.text_type)
                                                                                     and len(reset_w_type) <= reset_w_path.count(ROGlyph.NAME_SPACE_SEPARATOR)
                                                                                     )
                                                                                     or len(reset_w_type) <= len(reset_w_path)
                                                                                     )
            @precondition: reset_w_type is None or len(reset_w_type) > 0

            @see: glyphs.rw.RWGlyph.RWGlyph.__init__
        """
        super(ResettableGlyph, self).__init__(
                                              r_path,
                                              w_path,
                                              r_types,
                                              w_types,
                                              r_translation_function,
                                              w_translation_function,
                                              r_default_value,
                                              w_allow_none,
                                              )

        if reset_w_type is None:
            reset_w_type = w_types

        self.__dict__["__reset_w_path_type"] = self._generate_path_type_paired_sequence(reset_w_path, reset_w_type,)

        self.__dict__["__reset_value"] = reset_value

    @property
    def iter_reset_w_path_type(self):
        """
            Returns a new iterator through the configured sequence of triplet of the sub path, their matching
            types as a pair and a boolean expressing whether they are the last triplet in the sequence.

            The iterator makes up a typed path to reset write data into an object.

            @rtype: collections.Iterable

            @postcondition: next(return, None) is not None
            @postcondition: all(
                                (
                                    isinstance(x, tuple)
                                    and len(x) == 3
                                    and isinstance(x[0], bool)
                                    and isinstance(x[1], six.text_type) and len(x[1]) > 0
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
        return iter(self.__dict__["__reset_w_path_type"])

    @property
    def reset_value(self):
        """
            Gets the value indicating a reset for this entity.
        """
        return self.__dict__["__reset_value"]
