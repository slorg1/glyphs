from __future__ import unicode_literals

import collections
import itertools

from glyphs.helpers.ImmutableObject import ImmutableObject


class ROGlyph(ImmutableObject):
    """
        R/O glyph designed to read data from an object (source of the data).
    """

    NAME_SPACE_SEPARATOR = '>'
    """
        Token used to separate the 'levels' for the keys-value pairs.
    """

    KEY_VALUE_SEPARATOR = ':'
    """
        Token used to separate the key and values for the key-value pairs.
    """

    def __init__(self, r_path, r_types=None, r_translation_function=None, r_default_value=None):
        """
            Initializer for a R/O glyph.

            @param r_path: The "path" pointing to the source of data.
            For multilevel keys (nest level):
            - if the path is a unicode, use L{a name space separator<glyphs.api.ROGlyph.ROGlyph.NAME_SPACE_SEPARATOR>}
            between the various level of keys.
            - if the path is a collection, each level is a unicode in the collection.
            @type r_path: unicode or collections.Sequence
            @param r_types: (Optional) A string describing the type of data expected to be found in the
            source data. For each matching level in L{r_path}, a key-value pair may be specified, not all
            levels are required to have a type defined.
            - if L{r_types} is a unicode, use L{a name space separator<glyphs.api.ROGlyph.ROGlyph.NAME_SPACE_SEPARATOR>}
            between the various level of types. To omit a level of type, do not specify a key-value pair.
            - if L{r_types} is a collection, each level of types is a unicode in the collection. To omit a
            level of type, place C{None} at the skipped level.

            The level of types are key-value pairs. The key defines where the type information can be found at
            a given level in the source. The values specifies the type expected. The key and value separator
            <glyphs.api.ROGlyph.ROGlyph.KEY_VALUE_SEPARATOR>}.
            There is no need to specify every level of type to match L{r_path},
            as any long-tail levels that are not specified will be interpreted as having no key-value
            pairs.
            @param r_translation_function: function used to translate the data found at L{r_path}
            to any target format.
            This is meant to be a very simple function for pure translate / transtyping. No intelligence here.
            If C{None}, then no translation is needed and the data should be passed through.
            @param r_default_value: value to use as a default value. To be used when no data is found at
            L{r_path}.

            @precondition: isinstance(r_path, unicode) or all(isinstance(u, unicode) for u in r_path)
            @precondition: len(r_path) > 0
            @precondition: r_types is None or isinstance(r_types, (unicode, tuple))
            @precondition: r_types is None or len(r_types) > 0
            @precondition: r_types is None or isinstance(r_types, tuple) or (
                                                                                     (
                                                                                     isinstance(r_path, unicode)
                                                                                     and r_types.count(ROGlyph.NAME_SPACE_SEPARATOR) <= r_path.count(ROGlyph.NAME_SPACE_SEPARATOR)
                                                                                     )
                                                                                     or r_types.count(ROGlyph.NAME_SPACE_SEPARATOR) <= len(r_path)
                                                                                     )
            @precondition: r_types is None or isinstance(r_types, unicode) or (
                                                                                     (
                                                                                     isinstance(r_path, unicode)
                                                                                     and len(r_types) <= r_path.count(ROGlyph.NAME_SPACE_SEPARATOR)
                                                                                     )
                                                                                     or len(r_types) <= len(r_path)
                                                                                     )
            @precondition: r_types is None or len(r_types) > 0
            @precondition: r_translation_function is None or callable(r_translation_function)
        """
        assert r_translation_function is None or callable(r_translation_function)

        self.__dict__["__r_path_type"] = self._generate_path_type_paired_sequence(r_path, r_types,)

        self.__dict__["__r_translation_function"] = r_translation_function
        self.__dict__["__r_default_value"] = r_default_value

    def __repr__(self):
        return "{}({},)".format(self.__class__.name, self.r_path,)

    @property
    def iter_r_path_type(self):
        """
            Returns a new iterator through the configured sequence of triplet of the sub path, their matching
            types as a pair and a boolean expressing whether they are the last triplet in the sequence.

            The iterator makes up a typed path to read data out of an object.

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
        return iter(self.__dict__["__r_path_type"])

    @property
    def r_default_value(self):
        """
            Returns a value to use in case no suitable value is found in the object.
        """
        return self.__dict__["__r_default_value"]

    @property
    def r_translation_function(self):
        """
            Returns a function used to translate the value found in the object to a target
            format.

            Note: this is meant to be a very simple function for pure translate / transtyping. No
            intelligence here.

            If C{None}, then no translation is needed and the data should be passed through.

            @postcondition: return is None or callable(return)
        """
        return self.__dict__["__r_translation_function"]

    def _generate_path_type_paired_sequence(self, path, types,):
        """
            Returns a sequence of triplet of the sub path, their matching L{types} as a pair and a boolean expressing whether
            they are the last triplet in the sequence.

            @param path: The "path" to walk to reach the data.
            For multilevel keys (nest level):
            - if the path is a unicode, uses L{a name space separator<glyphs.api.ROGlyph.ROGlyph.NAME_SPACE_SEPARATOR>}
            between the various level of keys.
            - if the path is a collection, each level is a unicode in the collection.
            @type path: unicode or collections.Sequence
            @param types: (Optional) A string describing the type of data expected to be found in the
            source data. For each matching level in L{path} (sub path), a key-value pair may be specified, not
            all levels are required to have a type defined.
            - if L{types} is a unicode, uses L{a name space separator<glyphs.api.ROGlyph.ROGlyph.NAME_SPACE_SEPARATOR>}
            between the various level of types. To omit a level of type, do not specify a key-value pair at
            that level.
            - if L{types} is a collection, each level of types is a unicode in the collection. To omit a
            level of type, place C{None} at the skipped level.

            The level of types are key-value pairs. The key defines where the type information can be found at
            a given level in the source. The values specifies the type expected. The key and value separator
            <glyphs.api.ROGlyph.ROGlyph.KEY_VALUE_SEPARATOR>}.
            There is no need to specify every level of type to match L{path},
            as any long-tail levels that are not specified will be interpreted as having no key-value
            pairs.

            e.g.
            if the separator is a period '.' as a name space separator and ':' as a key separator to express
            and object which is a series of nested dictionaries:
            path: sub_path1.sub_path2.sub_path3
            value: 1
            types: ..xsi:Entity
            object: {'sub_path1': {'sub_path2': {'sub_path3': 1, 'xsi':'Entity' } } }

            @rtype: collections.Sequence

            @precondition: types is None or isinstance(types, tuple) or (
                                                                             (
                                                                             isinstance(path, unicode)
                                                                             and types.count(ROGlyph.NAME_SPACE_SEPARATOR) <= path.count(ROGlyph.NAME_SPACE_SEPARATOR)
                                                                             )
                                                                             or types.count(ROGlyph.NAME_SPACE_SEPARATOR) <= len(path)
                                                                        )
            @precondition: types is None or isinstance(types, unicode) or (
                                                                             (
                                                                             isinstance(path, unicode)
                                                                             and len(types) <= path.count(ROGlyph.NAME_SPACE_SEPARATOR)
                                                                             )
                                                                             or len(types) <= len(path)
                                                                          )
            @precondition: types is None or len(types) > 0

            @postcondition: len(return) > 0
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

        if isinstance(path, unicode):
            path_tuple = tuple(path.split(ROGlyph.NAME_SPACE_SEPARATOR))
        else:
            assert isinstance(path, collections.Sequence) # pre
            path_tuple = tuple(path)
            assert all(isinstance(u, unicode) for u in path_tuple) # pre

        assert path_tuple

        max_index = len(path_tuple) - 1


        if types is None:
            return None

        if isinstance(types, unicode):
            types_tuple = tuple(None if x == '' else x for x in types.split(ROGlyph.NAME_SPACE_SEPARATOR))
        else:
            assert isinstance(types, tuple)
            assert all(l is None or isinstance(l, unicode) for l in types)
            types_tuple = types

        # If this glyph is created with types_tuple, but they're all None (or we got a tuple of Nones)
        # let's revert it from the tuple back to None, to save cycles when the glyph is used
        # for setting values. This would happen if someone gave '..' as the types_tuple
        if all(t is None for t in types_tuple):
            return None

        assert types_tuple

        types_tuple = tuple(None if x is None else tuple(x.split(ROGlyph.KEY_VALUE_SEPARATOR)) for x in types_tuple)

        if len(types_tuple) < len(path_tuple):
            # pad anything that has been left unspecified.
            types_tuple += (None,) * (len(path_tuple) - len(types_tuple))
        else:
            assert len(types_tuple) == len(path_tuple) # pre

        assert len(types_tuple) == len(path_tuple) # dev check

        return tuple(
                      (idx == max_index, sub_path, type_name,)
                      for idx, (sub_path, type_name,) in enumerate(
                                                                  itertools.izip(
                                                                                 path_tuple,
                                                                                 types_tuple,
                                                                                 )
                                                                   )
                      )
