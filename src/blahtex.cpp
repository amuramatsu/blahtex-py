/*
 BSD 3-Clause License
 
 Copyright (c) 2020, MURAMATSU Atshshi
 All rights reserved.
 
 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are met:
 
 1. Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

 2. Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

 3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#include <BlahtexCore/Interface.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(_blahtex, m) {
    m.doc() = "Blahtex binding for python";

    static py::exception<blahtex::Exception> ex(m, "BlahtexException");
    py::register_exception_translator([](std::exception_ptr p){
	try {
	    if (p) std::rethrow_exception(p);
	} catch (const blahtex::Exception &e) {
	    std::wstring msg = e.GetCode() + L": ";
	    bool firstarg = true;
	    for (std::wstring arg: e.GetArgs()) {
		if (! firstarg)
		    msg += L", ";
		msg += arg;
		firstarg = false;
	    }
	    PyErr_SetObject(ex.ptr(),
			    PyUnicode_FromWideChar(msg.c_str(), msg.size()));
	}
    });
    
    py::class_<blahtex::Interface>(m, "Blahtex")
	.def(py::init<>())
	.def("process_input",
	     &blahtex::Interface::ProcessInput,
	     py::arg("input"), py::arg("display_style") = false)
	.def("get_mathml", &blahtex::Interface::GetMathml)
	.def("get_purified_tex", &blahtex::Interface::GetPurifiedTex)
	.def("get_purified_tex_only", &blahtex::Interface::GetPurifiedTexOnly)
	.def_readwrite("mathml_options",
		       &blahtex::Interface::mMathmlOptions)
	.def_readwrite("encoding_options",
		       &blahtex::Interface::mEncodingOptions)
	.def_readwrite("purified_tex_options",
		       &blahtex::Interface::mPurifiedTexOptions)
	.def_readwrite("texvc_compatibility",
		       &blahtex::Interface::mTexvcCompatibility)
	.def_readwrite("indented", &blahtex::Interface::mIndented);

    py::class_<blahtex::MathmlOptions> mathml_options(m, "MathmlOptions");
    mathml_options
	.def(py::init<>())
	.def_readwrite("spacing_control",
		       &blahtex::MathmlOptions::mSpacingControl)
	.def_readwrite("use_version1_font_attributes",
		       &blahtex::MathmlOptions::mUseVersion1FontAttributes)
	.def_readwrite("allow_plane1",
		       &blahtex::MathmlOptions::mAllowPlane1);
    py::enum_<blahtex::MathmlOptions::SpacingControl>(mathml_options,
						   "SpacingControl")
	.value("STRICT",
	       blahtex::MathmlOptions::SpacingControl::cSpacingControlStrict)
	.value("MODERATE",
	       blahtex::MathmlOptions::SpacingControl::cSpacingControlModerate)
	.value("RELAXED",
	       blahtex::MathmlOptions::SpacingControl::cSpacingControlRelaxed)
	.export_values();
    
    py::class_<blahtex::EncodingOptions> encoding_options(m, "EncodingOptions");
    encoding_options
	.def(py::init<>())
	.def_readwrite("mathml_encoding",
		       &blahtex::EncodingOptions::mMathmlEncoding)
	.def_readwrite("other_encoding_raw",
		       &blahtex::EncodingOptions::mOtherEncodingRaw)
	.def_readwrite("allow_plane1",
		       &blahtex::EncodingOptions::mAllowPlane1);
    py::enum_<blahtex::EncodingOptions::MathmlEncoding>(encoding_options,
						       "MathmlEncoding")
	.value("RAW",
	       blahtex::EncodingOptions::MathmlEncoding::cMathmlEncodingRaw)
	.value("NUMERIC",
	       blahtex::EncodingOptions::MathmlEncoding::cMathmlEncodingNumeric)
	.value("SHORT",
	       blahtex::EncodingOptions::MathmlEncoding::cMathmlEncodingShort)
	.value("LONG",
	       blahtex::EncodingOptions::MathmlEncoding::cMathmlEncodingLong)
	.export_values();

    py::class_<blahtex::PurifiedTexOptions>(m, "PurifiedTexOptions")
	.def(py::init<>())
	.def_readwrite("display_math",
		       &blahtex::PurifiedTexOptions::mDisplayMath)
	.def_readwrite("allow_ucs",
		       &blahtex::PurifiedTexOptions::mAllowUcs)
	.def_readwrite("allow_cjk",
		       &blahtex::PurifiedTexOptions::mAllowCJK)
	.def_readwrite("allow_preview",
		       &blahtex::PurifiedTexOptions::mAllowPreview)
	.def_readwrite("japanese_font",
		       &blahtex::PurifiedTexOptions::mJapaneseFont)
	.def_readwrite("latex_preamble",
		       &blahtex::PurifiedTexOptions::mLaTeXPreamble)
	.def_readwrite("latex_before_math",
		       &blahtex::PurifiedTexOptions::mLaTeXBeforeMath);
}	
