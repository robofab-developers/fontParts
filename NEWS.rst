0.9.0 (released 2019-08-30)
---------------------------
This release only supports Python 3, if you need Python 2 support, use 0.8.9.

- 2019-08-30: Remove Python 2 support.
- 2019-08-30: Change rounding to always round to the higher number, matching what fontTools does for anything visual.


0.8.9 (released 2019-08-25)
---------------------------
- 2019-08-25: Simplify `removeOverlap` in fontShell
- 2019-08-25: Fixup dev-requirements

Note: This will be one of the last releases to support Python2.

0.8.8 (released 2019-08-23)
---------------------------
- 2019-08-23: Fix `removeOverlap` and add `removeOverlap` to fontShell.
- 2019-07-23: Added support for `fileStructure`, for UFOZ.
- 2019-06-07: Allow first point of a contour to be smooth.

0.8.7 (released 2019-06-04)
---------------------------
- 2019-06-04: Change `RemovedWarning` to `RemovedError`
- 2019-03-26: Set the first layer in `layerOrder` as the default layer for `font.interpolate`
- 2019-03-18: A missing glyph in a `get` or `del` now returns `KeyError`

0.8.6 (released 2019-03-15)
---------------------------
- 2019-03-15: Fixed how `bPoint` reports curve types, tangents are now reported as curve.
- 2019-01-30: Fix `OpenFont` in fontShell.
- 2019-01-15: One more fix for RFont (thanks @madig!)

0.8.5 (released 2018-12-17)
---------------------------
- 2018-12-17: Improve glyph insert, only clear if the glyph is already in the font.
- 2018-12-17: Fix for `RFont` and `fs`
- 2018-12-14: Added a `getFlatKerning` method to `Font`. Thanks @typemytype
- 2018-12-14: Fixed glyph order being modified when a glyph is overwritten (thanks @justvanrossum for reporting, @typemytype for fixing)

0.8.4 (released 2018-12-07)
---------------------------
- 2018-12-7: Fixed `setStartSegment` (thanks @typemytype!)

0.8.3 (released 2018-12-05)
---------------------------
- 2018-12-05: `insertSegment` and `insertBPoint` fixed. (thanks @typemytype!)

0.8.2 (released 2018-11-02)
---------------------------
- 2018-11-01: Change to using fonttools.ufoLib
- 2018-10-16: Make compatibility checking for components and anchors more precise (WIP). Thank you @madig

0.8.1 (released 2018-09-20)
---------------------------
- 2018-09-20: Restyled the documentation, thanks @vannavu and @thundernixon
- 2018-09-12: Fixed Travis setup for OSX.
- 2018-09-06: All tests for ``Groups``.
- 2018-09-03: Fixed ``font.round()``.
- 2018-08-30: All tests for ``Image``.

0.8.0 (released 2018-08-21)
---------------------------

- 2018-08-21: Changed behavior of getting margins for empty (no outlines or components) glyphs, now returns `None`. `#346 <https://github.com/robofab-developers/fontParts/pull/346>`_
- 2018-08-20: Add public methods to `mathInfo` in the Info object. `#344 <https://github.com/robofab-developers/fontParts/pull/344>`_

0.7.2 (released 2018-08-03)
---------------------------

- 2018-08-03: Allow contours to start and end on an offCurve. `#337 <https://github.com/robofab-developers/fontParts/pull/337>`_

0.7.1 (released 2018-08-02)
---------------------------

- 2018-07-24: Fixed bug in default values in ``BaseDict``. This fixes a bug with default values in ``Kerning`` and ``Groups``.
- 2018-06-28: Improved documentation for ``world.AllFonts``
- 2018-06-20: Fixed a bug in ``world.AllFonts``
- 2018-06-14: Fixed a bug, UFO file format version must be an ``int``.

0.7.0 (released 2018-06-11)
---------------------------

- 2018-06-08: Fixed a bug in ``__bool__`` in ``Image`` that would fail if there was no image data.
- 2018-06-08: Fixed a bug in setting the parents in appending a ``guideline`` to a ``Glyph`` or ``Font``.
- 2018-05-30: Fixed a bug in both the base and fontshell implementations of ``groups.side1KerningGroups``.
- 2018-05-30: Fixed a bug in both the base and fontshell implementations of ``groups.side2KerningGroups``.
- 2018-05-30: Fixed a several bugs in ``BaseDict`` that would return values that hadn't been normalized.
- 2018-05-30: Implemented ``font.__delitem__``
- 2018-05-30: Implemented ``font.__delitem__``.
- 2018-05-30: Implemented ``layer.__delitem__``.
- 2018-05-30: ``font.removeGlyph`` is now an alias for ``font.__delitem__``.
- 2018-05-30: ``layer.removeGlyph`` is now an alias for ``layer.__delitem__``.
- 2018-05-30: ``font.insertGlyph`` is now an alias for ``font.__setitem__``.
- 2018-05-30: ``layer.insertGlyph`` is now an alias for ``layer.__setitem__``.
- 2018-05-30: ``font.appendGuideline`` now accepts a guideline object.
- 2018-05-30: ``glyph.copy`` uses the new append API.
- 2018-05-30: ``glyph.appendGlyph`` uses the new append API.
- 2018-05-30: ``glyph.appendComponent`` now accepts a component object.
- 2018-05-30: ``glyph.appendAnchor`` now accepts and anchor object.
- 2018-05-30: ``glyph.appendGuideline`` now accepts a guideline object.
- 2018-05-30: ``contour.appendSegment`` now accepts a segment object.
- 2018-05-30: ``contour.appendBPoint`` now accepts a bPoint object.
- 2018-05-30: ``contour.appendPoint``  now accepts a point object.
- 2018-05-30: ``contour.insertSegment`` now accepts a segment object.
- 2018-05-30: ``contour.insertBPoint`` now accepts a bPoint object.
- 2018-05-30: ``contour.insertPoint`` now accepts a point object.
