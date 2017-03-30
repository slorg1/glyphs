from __future__ import unicode_literals

import collections
from glyphs.helpers.ImmutableType import ImmutableType
from glyphs.ro.ROGlyph import ROGlyph
from glyphs.rw.RWGlyph import RWGlyph
from glyphs.rw.ResettableGlyph import ResettableGlyph

import six


class DictUtils(six.with_metaclass(ImmutableType)):
    """
        Utility methods for working with glyphs and dictionaries.
    """

    @staticmethod
    def get(source, glyph, force_default_to_none=False):
        """
            Returns the value stored in the given L{source} if it has the B{full} L{path and
            types<glyphs.api.ROGlyph.ROGlyph.iter_r_path_type>} held by L{glyph}.

            Otherwise:
            - if any intermediary pieces of the path is not in L{source} raises a C{KeyError}
            - if only the last piece of the path is missing returns L{the default value<glyphs.api.ROGlyph.
            ROGlyph.default_return>}.

            Any returned value is passed through the L{translation function of the glyph<glyphs.api.ROGlyph.
            ROGlyph.r_translation_function>} if one exists.

            If a call to L{DictUtils.in_} with the same L{source} and L{glyph} returns C{False}, this method
            will throw an error.
            If a call to L{DictUtils.in_} with the same L{source} and L{glyph} returns C{True}, this method
            will not throw an error and return a value (defaulted or translated)

            @type source: collections.Mapping
            @type glyph: ROGlyph
            @param force_default_to_none: If C{True}, L{default_return} will be returned if the 'raw' value
            found is C{None} (checked before translation function is applied).

            @raise KeyError: if any intermediary pieces of the path is not in L{source}
            @raise TypeError: if any intermediary pieces of the path does not match the expected type found in L{source}
        """
        Mapping = collections.Mapping
        assert isinstance(source, Mapping)
        assert isinstance(glyph, ROGlyph)

        # other preconditions tested below

        current_dict = source
        Container = collections.Container
        default_return = glyph.r_default_value

        for sub_path, source_type in glyph.iter_r_path_type:

            if not isinstance(current_dict, Mapping):
                raise KeyError('Could not find {} in the given dictionary'.format(sub_path))

            if isinstance(source_type, tuple):
                key = source_type[0]

                if (key not in current_dict
                    or isinstance(current_dict[key], Container) # saving the serialization cost as it is not going to work
                    or source_type[1] != unicode(current_dict[key])):
                    raise TypeError('Type mismatch for {} in the given dictionary'.format(sub_path))
            else:
                assert source_type is None

            # Cannot be current_dict.get() because not all collections.Mapping have get().
            current_dict = current_dict[sub_path] if sub_path in current_dict else default_return

        if (
            current_dict == default_return # type could be different in the case of string vs unicode.
            or (force_default_to_none and current_dict is None)
            ):
            return default_return

        t = glyph.r_translation_function
        if t and current_dict is not None:
            return t(current_dict)

        return current_dict

    @staticmethod
    def in_(source, glyph):
        """
            Returns  C{True} if the given L{source} has the B{full} L{path and types<glyphs.api.ROGlyph.
            ROGlyph.iter_r_path_type>} held by L{glyph}. Otherwise, returns C{False}.

            @type source: collections.Mapping
            @type glyph: ROGlyph

            @rtype: BooleanType
        """
        Mapping = collections.Mapping
        assert isinstance(source, Mapping)

        assert isinstance(glyph, ROGlyph)
        # other preconditions tested below

        current_dict = source
        Container = collections.Container
        iter_r_path_type = glyph.iter_r_path_type
        is_last = False

        for is_last, sub_path, source_type in iter_r_path_type:
            if isinstance(source_type, tuple):
                assert len(source_type) == 2

                key = source_type[0]

                if (
                    key not in current_dict
                    or isinstance(current_dict[key], Container) # saving the serialization cost as it is not going to work
                    or source_type[1] != unicode(current_dict[key])
                    ):
                    return False
            else:
                assert source_type is None

            if sub_path in current_dict:
                current_dict = current_dict[sub_path]
            else:
                return False

        return is_last

    @staticmethod
    def set(destination, glyph, value):
        """
            Sets the given L{value} in the L{destination} using L{utils.api.APIGlyph.APIGlyph.
            target_source_names}.

            The value is translated using L{utils.api.APIGlyph.APIGlyph.target_translation_func} if any is found. It is
            set 'raw' otherwise.

            If the L{value} or the translated value is C{None} then this method is a NOOP.

            @type destination: collections.MutableMapping
            @type glyph: APIGlyph

        """
        assert isinstance(glyph, RWGlyph)

        if glyph.w_translation_function:
            value = glyph.w_translation_function(value)

        if value is not None or glyph.w_allow_none:
            DictUtils.__set(destination, glyph.iter_w_path_type, value)

    @staticmethod
    def set_reset_value(destination, glyph):
        """
            Sets the L{reset value of the glyph<utils.api.AbstractResettableGlyph
            .AbstractResettableGlyph.reset_value>}, which will be interpreted by the API as a
            'reset', in the L{destination} using L{the reset source names of the glyph<utils.api
            .AbstractResettableGlyph.AbstractResettableGlyph.reset_target_source_names>} and
            the L{target type names<utils.api.APIGlyph.APIGlyph.target_type_names>}.

            @type destination: collections.MutableMapping
            @type glyph: AbstractResettableGlyph
        """
        assert isinstance(glyph, ResettableGlyph)
        # other preconditions tested in called func

        # when resetting, the reset value may not always be at the same place as the target type,
        # so we have to allow the depth mismatch
        DictUtils.__set(destination, glyph.iter_reset_w_path_type, glyph.reset_value,)

    @staticmethod
    def __set(destination, w_path_type, value,):
        """
            Sets the given L{value} in the L{destination} using L{target_source_names}.

            It recursively builds the sub dictionaries if the number of source names is greater than
            one. Each name is then used as L{depth} in the L{destination}. When on the last element
            of L{target_source_names} the key and value from L{root_type_key_values} is set and the
            method returns.

            @type destination: collections.MutableMapping
            @param root_type_key_values: Describes the key and value, or lack thereof, of all levels.
            @type root_type_key_values: tuple
            @type target_source_names: tuple
            @type depth: int

            @precondition: next(w_path_type, None,) is not None
        """
        assert isinstance(destination, collections.MutableMapping), type(destination)
        # other preconditions tested below

        is_last, sub_path, type_tuple, = next(w_path_type,)

        if is_last is False:
            sub_dict = destination.get(sub_path)
            if sub_dict is None:
                sub_dict = {}
                destination[sub_path] = sub_dict
                if type_tuple is not None:
                    key, value, = type_tuple

                    if key not in destination:
                        destination[key] = value
                    else:
                        # dev check
                        assert destination[key] == value

            DictUtils.__set(sub_dict, w_path_type, value,)
            return

        if type_tuple is not None:
            key, value, = type_tuple

            if key not in destination:
                destination[key] = value
            else:
                # dev check
                assert destination[key] == value

        destination[sub_path] = value

    __slots__ = tuple()
