
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
