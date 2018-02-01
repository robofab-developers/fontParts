import weakref
from fontTools.misc import transform
from fontParts.base import normalizers
from fontParts.base.base import (
    BaseObject, TransformationMixin, dynamicProperty, PointPositionMixin)
from fontParts.base.errors import FontPartsError
from fontParts.base.color import Color
from fontParts.base.deprecated import DeprecatedAnchor, RemovedAnchor


class BaseAnchor(BaseObject, TransformationMixin, DeprecatedAnchor, RemovedAnchor, PointPositionMixin):

    """
    An anchor object. This object is almost always
    created with :meth:`BaseGlyph.appendAnchor`.
    An orphan anchor can be created like this::

        >>> anchor = RAnchor()
    """

    def _reprContents(self):
        contents = [
            ("({x}, {y})".format(x=self.x, y=self.y)),
        ]
        if self.name is not None:
            contents.append("name='%s'" % self.name)
        if self.color:
            contents.append("color=%r" % str(self.color))
        return contents

    # ----
    # Copy
    # ----

    copyAttributes = (
        "x",
        "y",
        "name",
        "color"
    )

    # -------
    # Parents
    # -------

    def getParent(self):
        """
        Return the anchor's parent :class:`fontParts.base.BaseGlyph`.
        This is a backwards compatibility method.
        """
        return self.glyph

    # Glyph

    _glyph = None

    glyph = dynamicProperty("glyph", "The anchor's parent :class:`BaseGlyph`.")

    def _get_glyph(self):
        if self._glyph is None:
            return None
        return self._glyph()

    def _set_glyph(self, glyph):
        assert self._glyph is None
        if glyph is not None:
            glyph = weakref.ref(glyph)
        self._glyph = glyph

    # Layer

    layer = dynamicProperty("layer", "The anchor's parent :class:`BaseLayer`.")

    def _get_layer(self):
        if self._glyph is None:
            return None
        return self.glyph.layer

    # Font

    font = dynamicProperty("font", "The anchor's parent :class:`BaseFont`.")

    def _get_font(self):
        if self._glyph is None:
            return None
        return self.glyph.font

    # --------
    # Position
    # --------

    # x

    x = dynamicProperty(
        "base_x",
        """
        The x coordinate of the anchor.
        It must be an :ref:`type-int-float`. ::

            >>> anchor.x
            100
            >>> anchor.x = 101
        """
    )

    def _get_base_x(self):
        value = self._get_x()
        value = normalizers.normalizeX(value)
        return value

    def _set_base_x(self, value):
        value = normalizers.normalizeX(value)
        self._set_x(value)

    def _get_x(self):
        """
        This is the environment implementation of
        :attr:`BaseAnchor.x`. This must return an
        :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_x(self, value):
        """
        This is the environment implementation of
        :attr:`BaseAnchor.x`. **value** will be
        an :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # y

    y = dynamicProperty(
        "base_y",
        """
        The y coordinate of the anchor.
        It must be an :ref:`type-int-float`. ::

            >>> anchor.y
            100
            >>> anchor.y = 101
        """
    )

    def _get_base_y(self):
        value = self._get_y()
        value = normalizers.normalizeY(value)
        return value

    def _set_base_y(self, value):
        value = normalizers.normalizeY(value)
        self._set_y(value)

    def _get_y(self):
        """
        This is the environment implementation of
        :attr:`BaseAnchor.y`. This must return an
        :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_y(self, value):
        """
        This is the environment implementation of
        :attr:`BaseAnchor.y`. **value** will be
        an :ref:`type-int-float`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # --------------
    # Identification
    # --------------

    # index

    index = dynamicProperty(
        "base_index",
        """
        The index of the anchor within the ordered
        list of the parent glyph's anchors. This
        attribute is read only. ::

            >>> anchor.index
            0
        """
    )

    def _get_base_index(self):
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

    def _get_index(self):
        """
        Get the anchor's index.
        This must return an ``int``.

        Subclasses may override this method.
        """
        glyph = self.glyph
        if glyph is None:
            return None
        return glyph.anchors.index(self)

    # identifier

    identifier = dynamicProperty(
        "base_identifier",
        """
        The unique identifier for the anchor.
        This value will be an :ref:`type-identifier` or `None`.
        This attribute is read only. ::

            >>> anchor.identifier
            'ILHGJlygfds'

        To request an identifier if it does not exist use
        `anchor.getIdentifier()`
        """
    )

    def _get_base_identifier(self):
        value = self._get_identifier()
        value = normalizers.normalizeIdentifier(value)
        return value

    def _get_identifier(self):
        """
        This is the environment implementation of
        :attr:`BaseAnchor.identifier`. This must
        return an :ref:`type-identifier` or `None`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def getIdentifier(self):
        """
        Create a new, unique identifier for and assign it to the anchor.
        If the anchor already has an identifier, the existing one should be returned.
        """
        return self._getIdentifier()

    def _getIdentifier(self):
        """
        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # name

    name = dynamicProperty(
        "base_name",
        """
        The name of the anchor. This will be a
        :ref:`type-string` or ``None``.

            >>> anchor.name
            'my anchor'
            >>> anchor.name = None
        """
    )

    def _get_base_name(self):
        value = self._get_name()
        if value is not None:
            value = normalizers.normalizeAnchorName(value)
        return value

    def _set_base_name(self, value):
        if value is not None:
            value = normalizers.normalizeAnchorName(value)
        self._set_name(value)

    def _get_name(self):
        """
        This is the environment implementation of
        :attr:`BaseAnchor.name`. This must return a
        :ref:`type-string` or ``None``. The returned
        value will be normalized with
        :func:`normalizers.normalizeAnchorName`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_name(self, value):
        """
        This is the environment implementation of
        :attr:`BaseAnchor.name`. **value** will be
        a :ref:`type-string` or ``None``. It will
        have been normalized with
        :func:`normalizers.normalizeAnchorName`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # color

    color = dynamicProperty(
        "base_color",
        """
        The anchor's color. This will be a
        :ref:`type-color` or ``None``. ::

            >>> anchor.color
            None
            >>> anchor.color = (1, 0, 0, 0.5)
        """
    )

    def _get_base_color(self):
        value = self._get_color()
        if value is not None:
            value = normalizers.normalizeColor(value)
            value = Color(value)
        return value

    def _set_base_color(self, value):
        if value is not None:
            value = normalizers.normalizeColor(value)
        self._set_color(value)

    def _get_color(self):
        """
        This is the environment implementation of
        :attr:`BaseAnchor.color`. This must return
        a :ref:`type-color` or ``None``. The
        returned value will be normalized with
        :func:`normalizers.normalizeColor`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    def _set_color(self, value):
        """
        This is the environment implementation of
        :attr:`BaseAnchor.color`. **value** will
        be a :ref:`type-color` or ``None``.
        It will have been normalized with
        :func:`normalizers.normalizeColor`.

        Subclasses must override this method.
        """
        self.raiseNotImplementedError()

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, origin=None, originOffset=None, **kwargs):
        """
        This is the environment implementation of
        :meth:`BaseAnchor.transformBy`.

        **matrix** will be a :ref:`type-transformation`.
        that has been normalized with :func:`normalizers.normalizeTransformationMatrix`.
        **origin** will be a :ref:`type-coordinate` defining
        the point at which the transformation should originate.
        **originOffset** will be a pre-calculated offset
        (x, y) that represents the deltas necessary to
        realign the post-transformation origin point
        with the pre-transformation origin point.

        Subclasses may override this method.
        """
        t = transform.Transform(*matrix)
        x, y = t.transformPoint((self.x, self.y))
        self.x = x
        self.y = y
        if originOffset != (0, 0):
            self.moveBy(originOffset)

    # -------------
    # Normalization
    # -------------

    def round(self):
        """
        Round the anchor's coordinate.

            >>> anchor.round()

        This applies to the following:

        * x
        * y
        """
        self._round()

    def _round(self):
        """
        This is the environment implementation of
        :meth:`BaseAnchor.round`.

        Subclasses may override this method.
        """
        self.x = normalizers.normalizeRounding(self.x)
        self.y = normalizers.normalizeRounding(self.y)
