# BSD 3-Clause License
#
# Copyright (c) 2020, MURAMATSU Atshshi
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from . import _blahtex # type: ignore
import enum
import textwrap

BlahtexException = _blahtex.BlahtexException

class Blahtex(object):
    '''
    Usage
    =====

    >> from blahtex import Blahtex
    >> bl = Blahtex(spacing=Blatex.SPACING.RELAXED)
    >> bl.indented = True
    >> bl.convert(r'\sqrt{3} * \pi')
    '<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msqrt><mn>3</mn></msqrt><mo>*</mo><mi>π</mi></mrow></math>'

    Options
    -------

    The options of blahtex are appeared by method variables of Blatex object.

    indented: bool
        Output of each MathML tag on a separate line, with indenting.

        Default is False.

    texvc_compatibility: bool
        Enables use of commands thar are specific to texvc, but that are not
        standard TeX/LaTeX/AMS-LaTeX commands

        Default is False.

    spacing: Blatex.SPACING
        Controls how much MathML spacing markup to use (i.e. ``<mspace>`` tags,
        and ``lspace/rspace`` attributes). Blahtex always uses TeX's rules
        (or an approximation thereof) to compute how much space to place
        between symbols in the equation, but this option describes how often
        it will actually emit MathML spacing markup to implement its spacing
        decisions.

        Blatex.SPACING.STRICT
            Output spacing markup everywhere possible; leave as little choice
            as possible to the MathML renderer. This will result in the most
            bloated output, but hopefully will look as much like TeX output as
            possible.

        Blatex.SPACING.MODERATE
            Output spacing commands whenever blahtex thinks a typical MathML
            renderer is likely to do something visually unsatisfactory without
            additional help. The aim is to get good agree- ment with TeX
            without overly bloated MathML markup. (It's very difficult to get
            this right, so I expect it to be under continual review.)

        Blatex.SPACING.RELAXED
            Only output spacing commands when the user specifically asks for
            them, using TeX commands like ``\,`` or ``\quad``.

        Default is Blatex.SPACING.RELAXED

        The magic command ``\strictspacing`` will override this setting.

    disallow_plane_1: bool
        Any characters that is not placed at Unicode BMP plane is replaced by
        XML numeric entries or not.

        Default is False.

    mathml_encoding: Blatex.ENCODING
        Controls the way blahtex output MathML charaters.
        
        Blatex.ENCODING.RAW
            Output unicode characters.
        Blatex.ENCODING.NUMERIC
            Use XML numeric entries.
        Blatex.ENCODING.SHORT
            Use **short** MathML entity names.
        Blatex.ENCODING.lONG
            Use **long** MathML entity names.

        Default is Blatex.ENCODING.RAW

    other_encoding: Blatex.ENCODING
        Controls the way blahtex output charaters except for ASCII/MathML
        charaters.
        
        Blatex.ENCODING.RAW
            Output unicode characters.
        Blatex.ENCODING.NUMERIC
            Use XML numeric entries.

        Default is Blatex.ENCODING.RAW

    mathml_version1_fonts: bool
        Forbids use of the ``mathvariant`` attribute, which is only avaiable
        in MathML 2.0 or later. Instead, blahtex will use MathML version 1.x
        font attributes: ``fontfamily``, ``fontstyle`` and ``fontweight``,
        which are all deprecated in MathML 2.0.

        Default is False.
    '''

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
        '''Constructor.

        You can set options by keyword arguments.
        '''
        super().__setattr__('_core', _blahtex.Blahtex())
        super().__setattr__('_inputted', False)
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
        '''Set options of blahtex.

        You can set options by keyword argument like as
        >> bl.set_options(indented=True)
        or by dictionay like as
        >> opts = { 'spacing': bl.SPACING.STRICT }
        >> bl.set_options(opts)  

        List of options is shown at docstring of this class.
        '''
        
        if len(args):
            if len(args) == 1 and isinstance(args[0], dict):
                opts = args[0]
            else:
                raise ValueError('Argument must be a dictionay '
                                 'or keyword argments')
        else:
            opts = kargs
        for k, v in opts.items():
            setattr(self, k, v)

    def get_options(self) -> dict:
        '''Get all options of blahtex.

        List of options is shown at docstring of this class.

        Returns
        -------
        dict
          Options
        '''
        result = {}
        for key in ("indented",  "texvc_compatibility", "spacing",
                    "disallow_plane_1", "mathml_encoding", "other_encoding",
                    "mathml_version1_fonts",
                    "use_ucs_package", "use_cjk_package", "use_preview_package",
                    "japanese_font", "latex_preamble", "latex_before_math"):
            result[key] = getattr(self, key)
        return result

    def process_input(self, s: str, display_math: bool=False) -> None:
        '''Set input TeX-string to blahtex.

        Paramters
        ---------
        s : str
          TeX/LaTeX/AMS-LaTeX string. Supported commands are listed on
          a document of blahtex-0.9.
        display_math: bool=Flase
          Input string are assumed at display-math environment. When this
          argmuent is False (default), TeX-stirng is assumed at inline-math.

        Raises
        ------
        BlahtexException
          If s is not recognized by blahtex.
        '''
        super().__setattr__('_inputted', True)
        self._core.purified_tex_options.display_math = display_math
        self._core.process_input(s, display_math)
    
    def get_mathml(self) -> str:
        '''Get MathML string converted by blahtex.

        Returns
        -------
        str
          MathML converted form TeX-string

        Raises
        ------
        ValueError
          If no TeX-string is inputted by ``process_input()``.
        '''
        if not self._inputted:
            raise ValueError("no TeX-string is processed")
        if self._core.purified_tex_options.display_math:
            display = "block"
        else:
            display = "inline"
        head = ('<math xmlns="http://www.w3.org/1998/Math/MathML" ' +
                'display="{}">'.format(display))
        body = self._core.get_mathml()
        if self.indented:
            return head + "\n" + textwrap.indent(body, "  ") + "</math>\n"
        return head + body + "</math>"

    def get_purified_tex(self) -> str:
        if not self._inputted:
            raise ValueError("no TeX-string is processed")
        return self._core.get_purified_tex()

    def get_purified_tex_only(self) -> str:
        if not self._inputted:
            raise ValueError("no TeX-string is processed")
        return self._core.get_purified_tex_only()

    def convert(self, latex: str, display_math: bool=False) -> str:
        '''Convert TeX-string to MathML.

        Paramters
        ---------
        s : str
          TeX/LaTeX/AMS-LaTeX string. Supported commands are listed on
          a document of blahtex-0.9.
        display_math: bool=Flase
          Input string are assumed at display-math environment. When this
          argmuent is False (default), TeX-stirng is assumed at inline-math.

        Returns
        -------
        str
          MathML converted form TeX-string

        Raises
        ------
        BlahtexException
          If s is not recognized by blahtex.
        '''
        self.process_input(latex, display_math)
        return self.get_mathml()
