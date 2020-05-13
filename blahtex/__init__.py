#
#
#

from . import _blahtex
import enum

class Blahtex(object):

    class ENCODING(enum.Enum):
        RAW = 0
        NUMERIC = 1
        SHORT = 2
        LONG = 3

    class SPACING(enum.Enum):
        STRICT = 0
        MODERATE = 1
        RELAXED = 2

    def __init__(self, **opts):
        super().__setattr__('_core', _blahtex.Blahtex())
        o = {
            "disallow_plane_1": False,
            "spacing": self.SPACING.RELAXED,
            "mathml_encoding": self.ENCODING.RAW,
            "other_encoding": self.ENCODING.RAW,
        }
        o.update(opts)
        self.set_options(o)

    def __setattr__(self, key, value):
        if key == "indented":
            self._core.indented = value
        elif key == "texvc_compatibility":
            self._core.texvc_compatibility = value
        elif key == "spacing":
            if value == self.SPACING.STRICT:
                v = _blahtex.MathmlOptions.SpacingControl.STRICT
            elif value == self.SPACING.MODERATE:
                v = _blahtex.MathmlOptions.SpacingControl.MODERATE
            elif value == self.SPACING.RELAXED:
                v = _blahtex.MathmlOptions.SpacingControl.RELAXED
            else:
                raise ValueError(
                    "spacing must be one of "
                    "Blahtex.SPACING.{STRICT,MODERATE,RELAXED}")
            self._core.mathml_options.spacing_control = v
        elif key == "disallow_plane_1":
            self._core.mathml_options.allow_plane1 = not value
            self._core.encoding_options.allow_plane1 = not value
        elif key == "mathml_encoding":
            if value == self.ENCODING.RAW:
                v = _blahtex.EncodingOptions.MathmlEncoding.RAW
            elif value == self.ENCODING.NUMERIC:
                v = _blahtex.EncodingOptions.MathmlEncoding.NUMERIC
            elif value == self.ENCODING.LONG:
                v = _blahtex.EncodingOptions.MathmlEncoding.LONG
            elif value == self.ENCODING.SHORT:
                v = _blahtex.EncodingOptions.MathmlEncoding.SHORT
            else:
                raise ValueError(
                    "mathml_encoding must be one of "
                    "Blahtex.ENCODING.{RAW,NUMERIC,LONG,SHORT}")
            self._core.encoding_options.mathml_encoding = v
        elif key == "other_encoding":
            if value == self.ENCODING.RAW:
                v = True
            elif value == self.ENCODING.NUMERIC:
                v = False
            else:
                raise ValueError(
                    "other_encoding must be one of "
                    "Blahtex.ENCODING.{RAW,NUMERIC}")
            self._core.encoding_options.other_encoding_raw = v
        elif key == "mathml_version1_fonts":
            self._core.mathml_options.use_version1_font_attributes = value
        elif key == "use_ucs_package":
            self._core.purified_tex_options.allow_ucs = value
        elif key == "use_cjk_package":
            self._core.purified_tex_options.allow_cjk = value
        elif key == "use_preview_package":
            self._core.purified_tex_options.allow_preview = value
        elif key == "japanese_font":
            self._core.purified_tex_options.japanese_font = value
        elif key == "latex_preamble":
            self._core.purified_tex_options.latex_preamble = value
        elif key == "latex_before_math":
            self._core.purified_tex_options.latex_before_math = value
        else:
            raise ValueError("Unknown attribute '{}'".format(key))
        
    def __getattr__(self, key):
        if key == "indented":
            return self._core.indented
        elif key == "texvc_compatibility":
            return self._core.texvc_compatibility
        elif key == "spacing":
            v = self._core.mathml_options.spacing_control
            if v == _blahtex.MathmlOptions.SpacingControl.STRICT:
                return self.SPACING.STRICT
            elif v == _blahtex.MathmlOptions.SpacingControl.MODERATE:
                return self.SPACING.MODERATE
            elif v == _blahtex.MathmlOptions.SpacingControl.RELAXED:
                return self.SPACING.RELAXED
            else:
                raise Exception()
        elif key == "disallow_plane_1":
            return not self._core.mathml_options.allow_plane1
        elif key == "mathml_encoding":
            v = self._core.encoding_options.mathml_encoding
            if v == _blahtex.EncodingOptions.MathmlEncoding.RAW:
                return self.ENCODING.RAW
            elif v == _blahtex.EncodingOptions.MathmlEncoding.NUMERIC:
                return self.ENCODING.NUMERIC
            elif v == _blahtex.EncodingOptions.MathmlEncoding.LONG:
                return self.ENCODING.LONG
            elif v == _blahtex.EncodingOptions.MathmlEncoding.SHORT:
                return self.ENCODING.SHORT
            else:
                raise Exception()
        elif key == "other_encoding":
            if self._core.encoding_options.other_encoding_raw:
                return self.ENCODING.RAW
            else:
                return self.ENCODING.NUMERIC
        elif key == "mathml_version1_fonts":
            return self._core.mathml_options.use_version1_font_attributes
        elif key == "use_ucs_package":
            return self._core.purified_tex_options.allow_ucs
        elif key == "use_cjk_package":
            return self._core.purified_tex_options.allow_cjk
        elif key == "use_preview_package":
            return self._core.purified_tex_options.allow_preview
        elif key == "japanese_font":
            return self._core.purified_tex_options.japanese_font
        elif key == "latex_preamble":
            return self._core.purified_tex_options.latex_preamble
        elif key == "latex_before_math":
            return self._core.purified_tex_options.latex_before_math

    def set_options(self, *args, **kargs) -> None:
        if len(args):
            if len(args) == 1 and isinstance(args[0], dict):
                opts = args[0]
            else:
                raise ValueError()
        else:
            opts = kargs
        for k, v in opts.items():
            setattr(self, k, v)

    def get_options(self) -> dict:
        result = {}
        for key in ("indented",  "texvc_compatibility", "spacing",
                    "disallow_plane_1", "mathml_encoding", "other_encoding",
                    "mathml_version1_fonts",
                    "use_ucs_package", "use_cjk_package", "use_preview_package",
                    "japanese_font", "latex_preamble", "latex_before_math"):
            result[key] = getattr(self, key)
        return result

    def process_input(self, s: str, display_math: bool=False) -> None:
        self._core.purified_tex_options.display_math = display_math
        self._core.process_input(s, display_math)
    
    def get_mathml(self) -> str:
        if self._core.purified_tex_options.display_math:
            display = "block"
        else:
            display = "inline"
        return ('<math xmlns="http://www.w3.org/1998/Math/MathML" ' +
                'display="{}">'.format(display) +
                self._core.get_mathml() + "</math>")

    def get_purified_tex(self) -> str:
        return self._core.get_purified_tex()

    def get_purified_tex_only(self) -> str:
        return self._core.get_purified_tex_only()

    def convert(self, latex: str, display_math: bool=False) -> str:
        self.process_input(latex, display_math)
        return self.get_mathml()
