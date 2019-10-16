from fontParts.base import BaseGlyph
from fontParts.base.errors import FontPartsError
from fontParts.fontshell.base import RBaseObject
from fontParts.opentype.contour import OTContour
from fontParts.opentype.component import OTComponent
# from fontParts.fontshell.point import RPoint
import defcon
from fontTools.pens.areaPen import AreaPen
import fontTools.ttLib.tables._g_l_y_f
from fontTools.ttLib.ttFont import _TTGlyph, _TTGlyphCFF
from fontTools.ttLib.tables._g_l_y_f import GlyphComponent
from fontTools.pens.recordingPen import RecordingPen

class OTGlyph(RBaseObject, BaseGlyph):
    wrapClass = fontTools.ttLib.ttFont._TTGlyph
    contourClass = OTContour
    componentClass = OTComponent

    def _init(self, *args, **kwargs):
        self._wrapped = kwargs["wrap"]
        self._name = kwargs["name"]
        self._contourlist = None

    # --------------
    # Identification
    # --------------

    # Name

    def _get_name(self):
        return self._name

    def _set_name(self, value):
        self._name = value

    # Unicodes

    def _get_unicodes(self):
        return list(self.font.naked()["cmap"].buildReversed()[self._name])

    def _set_unicodes(self, value):
        self.raiseNotImplementedError()

    # -------
    # Metrics
    # -------

    # horizontal

    def _get_width(self):
        return self.naked().width

    def _set_width(self, value):
        self.font.naked()["hmtx"][self._name] = (value, self.font.naked()["hmtx"][self._name][1])

    def _get_leftMargin(self):
        return self.font.naked()["hmtx"][self._name][1]

    def _set_leftMargin(self, value):
        oldLSB = self.font.naked()["hmtx"][self._name][1]
        delta = value - oldLSB
        oldWidth = self.width
        self.font.naked()["hmtx"][self._name] = (self.font.naked()["hmtx"][self._name][0], value)
        self.move((delta,0))
        self.width = oldWidth + delta

    def _get_rightMargin(self):
        return self.width - self.bounds[2]

    def _set_rightMargin(self, value):
        newWidth = self.bounds[2] + value
        self._set_width(newWidth)

    # vertical
    def _get_height(self):
        return self.font.naked()["hhea"].ascent
        # Or maybe self.font.naked()["OS/2"].usWinAscent

    def _set_height(self, value):
        self.font.naked()["hhea"].ascent = value

    # ------
    # Bounds
    # ------

    def _get_bounds(self):
        if hasattr(self.naked()._glyph, "calcBounds"): # CFF
            self._glyphset = self.font.naked().getGlyphSet()
            return self.naked()._glyph.calcBounds(self._glyphset)
        naked = self.naked()._glyph
        return (naked.xMin, naked.yMin, naked.xMax, naked.yMax)

    # ----
    # Area
    # ----
    def _get_area(self):
        pen = AreaPen()
        self.naked().draw(pen)
        return abs(pen.value)

    # ----
    # Pens
    # ----

    def getPen(self):
        from fontTools.pens.pointPen import SegmentToPointPen
        return SegmentToPointPen(self.getPointPen())

    def getPointPen(self):
        from fontTools.pens.pointPen import BasePointToSegmentPen
        return BasePointToSegmentPen()
        # return self.naked().getPointPen()

    # -----------------------------------------
    # Contour, Component and Anchor Interaction
    # -----------------------------------------

    # Contours

    def _contourStartAndEnd(self,index):
        glyph = self.naked()._glyph # XXX Only TTF
        endPt = glyph.endPtsOfContours[index]
        if index > 0:
            startPt = glyph.endPtsOfContours[index-1]
        else:
            startPt = 0
        return startPt, endPt

    def _lenContours(self, **kwargs):
        if isinstance(self.naked(), _TTGlyphCFF):
            self._build_CFF_contour_list()
            return len(self._contourlist)

        return max(self.naked()._glyph.numberOfContours,0)

    def _build_CFF_contour_list(self):
        if self._contourlist is None:
            pen = RecordingPen()
            self.naked().draw(pen)
            contours = pen.value
            lastcontour = []
            self._contourlist = []
            startPt = (0,0)
            lastPt = (0,0)
            index = 0
            for c in contours:
                if c[0] == "moveTo":
                    startPt = c[1][0]
                elif c[0] == "closePath":
                    if startPt != lastPt:
                        lastcontour.append(defcon.Point(startPt,segmentType = "line"))
                    contour = self.contourClass(wrap=lastcontour, index=index)
                    self._contourlist.append(contour)
                    index = index + 1
                    lastcontour = []
                elif c[0] == "curveTo":
                    lastcontour.append(defcon.Point(c[1][0],segmentType = "offcurve"))
                    lastcontour.append(defcon.Point(c[1][1],segmentType = "offcurve"))
                    lastcontour.append(defcon.Point(c[1][2],segmentType = "curve"))
                    lastPt = c[1][2]
                elif c[0] == "lineTo":
                    lastcontour.append(defcon.Point(c[1][0],segmentType = "line"))
                    lastPt = c[1][0]
                elif c[0] == "qCurveTo":
                    self.raiseNotImplementedError()

    def _getContour_CFF(self, index, **kwargs):
        self._build_CFF_contour_list()
        return self._contourlist[index]

    def _getContour(self, index, **kwargs):
        if isinstance(self.naked(), _TTGlyphCFF):
            return self._getContour_CFF(index)

        glyph = self.naked()._glyph
        startPt, endPt = self._contourStartAndEnd(index)
        contour = []
        for j in range(startPt, endPt+1):
            coords = (glyph.coordinates[j][0], glyph.coordinates[j][1])
            flags = glyph.flags[j] == 1
            t = "offcurve"
            if flags == 1:
                if (j == startPt and glyph.flags[endPt] == 1) or (j != startPt and contour[-1].segmentType != "offcurve"):
                    t = "line"
                else:
                    t = "curve"
            contour.append(defcon.Point(coords,segmentType = t))
        return self.contourClass(wrap=contour, index=index)

    def _setContour_CFF(self,index,contour):
        self._build_CFF_contour_list()
        self._contourlist[index] = contour
        from fontTools.pens.t2CharStringPen import T2CharStringPen
        width = 0 # self.width # Really?
        pen = T2CharStringPen(width, None)
        # ?
        for c in self._contourlist:
            pen.moveTo(c.segments[-1].points[-1])
            for s in c.segments:
                if s.type == "line":
                    pen.lineTo(*s.points)
                elif s.type == "curve" and len(s.points) == 3:
                    pen.curveTo(*s.points)
                elif s.type == "curve" and len(s.points) == 2:
                    pen.qCurveTo(*s.points)
            pen.closePath()
            cs = pen.getCharString()
            cs.private = self.font.naked()["CFF "].cff.topDictIndex[0].CharStrings[self.name].private
            self.font.naked()["CFF "].cff.topDictIndex[0].CharStrings[self.name] = cs

    def _setContour(self,index,contour):
        if isinstance(self.naked(), _TTGlyphCFF):
            return self._setContour_CFF(index,contour)
        old = self._getContour(index)
        clist = contour.naked()
        if len(old.naked()) != len(clist):
            self.raiseNotImplementedError()
        glyph = self.naked()._glyph
        startPt, endPt = self._contourStartAndEnd(index)
        for j in range(0,len(clist)):
            glyph.coordinates[j+startPt] = (clist[j].x,clist[j].y)
            glyph.flags[j+startPt] = int(clist[j].segmentType != "offcurve")
        glyph.recalcBounds(self.font.naked()["glyf"])

    def _removeContour(self, index, **kwargs):
        glyph = self.naked()
        contour = glyph[index]
        glyph.removeContour(contour)

    def _correctDirection(self, trueType=False, **kwargs):
        self.naked().correctContourDirection(trueType=trueType)

    # Components

    def _lenComponents(self, **kwargs):
        if hasattr(self.naked()._glyph,"components"):
            return len(self.naked()._glyph.components)
        return 0

    def _getComponent(self, index, **kwargs):
        glyph = self.naked()._glyph
        component = glyph.components[index]
        return self.componentClass(component)

    def _removeComponent(self, index, **kwargs): # XXX
        glyph = self.naked()._glyph
        if hasattr(self.naked()._glyph,"components"):
            return glyph.components.pop(index)

    def _appendComponent(self, baseGlyph, transformation=None, identifier=None, **kwargs):
        c = GlyphComponent()
        c.transformation = transformation
        c.glyphName = baseGlyph
        c.x = 0
        c.y = 0
        c.flags = 0 # XXX
        glyph = self.naked()._glyph
        if hasattr(self.naked()._glyph,"components"):
            glyph.components.append(c)
        else:
            glyph.components = [c]

    # Guidelines
    def _lenGuidelines(self, **kwargs):
        return 0 # len(self.naked().anchors)

    # Anchors XXX

    def _lenAnchors(self, **kwargs):
        return 0 # len(self.naked().anchors)

    def _getAnchor(self, index, **kwargs):
        return None

    def _appendAnchor(self, name, position=None, color=None, identifier=None, **kwargs):
        self.raiseNotImplementedError()

    def _removeAnchor(self, index, **kwargs):
        self.raiseNotImplementedError()

    # ----
    # Note
    # ----
    def _get_note(self):
        return None

    def _set_note(self, value):
        self.raiseNotImplementedError()

    # Mark
    def _get_markColor(self):
        return None

    def _set_markColor(self, value):
        self.raiseNotImplementedError()

    # -----------
    # Sub-Objects
    # -----------

    # lib

    def _get_lib(self):
        return None
    def _get_base_lib(self):
        return None
