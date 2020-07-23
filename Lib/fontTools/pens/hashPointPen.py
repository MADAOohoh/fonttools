# Modified from https://github.com/adobe-type-tools/psautohint/blob/08b346865710ed3c172f1eb581d6ef243b203f99/python/psautohint/ufoFont.py#L800-L838
import hashlib

from fontTools.pens.pointPen import AbstractPointPen
from fontTools.pens.transformPen import TransformPointPen


class HashPointPen(AbstractPointPen):
    """
    This pen can be used to check if a glyph's contents (outlines plus
    components) has changed.

    Components are decomposed, because that is what happens in TrueType
    hinting.
    """

    def __init__(self, glyph, glyphSet=None):
        self.glyphset = glyphSet
        self.width = round(getattr(glyph, "width", 0), 9)
        self.data = ["w%s" % self.width]

    @property
    def hash(self):
        data = "".join(self.data)
        if len(data) >= 128:
            data = hashlib.sha512(data.encode("ascii")).hexdigest()
        return data

    def beginPath(self, identifier=None, **kwargs):
        pass

    def endPath(self):
        self.data.append("|")

    def addPoint(
        self,
        pt,
        segmentType=None,
        smooth=False,
        name=None,
        identifier=None,
        **kwargs,
    ):
        if segmentType is None:
            pt_type = "o"  # offcurve
        else:
            pt_type = segmentType[0]
        self.data.append(f"{pt_type}{pt[0]:g}{pt[1]:+g}")

    def addComponent(
        self, baseGlyphName, transformation, identifier=None, **kwargs
    ):
        tpen = TransformPointPen(self, transformation)
        self.glyphset[baseGlyphName].drawPoints(tpen)
