anchorCases = """

>>>
+ id: Generic Anchor
+ object: Anchor = anchor
anchor.name = None
anchor.x = 1
anchor.y = 2
anchor.color = None
<<<

>>>
+ base: Generic Anchor
+ id: Test Anchor 1
anchor.name = "testAnchor1"
<<<

"""

from fontParts.base import FontPartsError
from fontParts.test.base.support import parseCases


class TestAnchor(object):

    cases = parseCases(anchorCases)

    # -----------
    # Environment
    # -----------

    def getCaseObjects(self, id):
        raise NotImplementedError

    # --------------
    # Identification
    # ---------------

    def test_name(self):
        caseObjects = self.getCaseObjects("Test Anchor 1")
        anchor = caseObjects["anchor"]
        # get
        self.assertEqual(
            anchor.name,
            "testAnchor1"
        )
        # set: valid
        anchor.name = u"foo"
        self.assertEqual(
            anchor.name,
            u"foo"
        )
        # set: invalid
        with self.assertRaises(FontPartsError):
            anchor.name = 123
