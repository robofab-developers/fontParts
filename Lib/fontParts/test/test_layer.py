import unittest
import collections
from fontParts.base import FontPartsError


class TestLayer(unittest.TestCase):

    # ------
    # Glyphs
    # ------

    def getLayer_glyphs(self):
        layer, _unrequested = self.objectGenerator("layer")
        for name in "ABCD":
            glyph = layer.newGlyph(name)
        return layer

    # len

    def test_len(self):
        layer = self.getLayer_glyphs()
        self.assertEqual(
            len(layer),
            4
        )

    # ----
    # Hash
    # ----
    def test_hash(self):
        layer = self.getLayer_glyphs()
        self.assertEqual(
            isinstance(layer, collections.Hashable),
            False
        )

    # --------
    # Equality
    # --------

    def test_equal(self):
        layer_one = self.getLayer_glyphs()
        layer_two = self.getLayer_glyphs()
        self.assertEqual(
            layer_one,
            layer_one
        )
        self.assertNotEqual(
            layer_one,
            layer_two
        )
        a = layer_one
        self.assertEqual(
            layer_one,
            a
        )
        self.assertNotEqual(
            layer_two,
            a
        )