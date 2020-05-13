#! /usr/bin/env python3
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import setuptools

__version__ = '0.0.1'


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __str__(self):
        import pybind11
        return pybind11.get_include()

ext_modules = [
    Extension(
        'blahtex._blahtex',
        # Sort input source files to ensure bit-for-bit reproducible builds
        # (https://github.com/pybind/python_example/pull/53)
        sorted([
            'src/blahtex.cpp',
	    'blahtexml/Source/BlahtexCore/InputSymbolTranslation.cpp',
	    'blahtexml/Source/BlahtexCore/Interface.cpp',
	    'blahtexml/Source/BlahtexCore/LayoutTree.cpp',
	    'blahtexml/Source/BlahtexCore/MacroProcessor.cpp',
	    'blahtexml/Source/BlahtexCore/Manager.cpp',
	    'blahtexml/Source/BlahtexCore/Parser.cpp',
	    'blahtexml/Source/BlahtexCore/ParseTree1.cpp',
	    'blahtexml/Source/BlahtexCore/ParseTree2.cpp',
	    'blahtexml/Source/BlahtexCore/ParseTree3.cpp',
	    'blahtexml/Source/BlahtexCore/MathmlNode.cpp',
	    'blahtexml/Source/BlahtexCore/Token.cpp',
	    'blahtexml/Source/BlahtexCore/XmlEncode.cpp',
        ]),
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            "blahtexml/Source",
            "blahtexml/Source/BlahtexCore",
        ],
        language='c++'
    ),
]

# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    import os
    with tempfile.NamedTemporaryFile('w', suffix='.cpp', delete=False) as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        fname = f.name
    try:
        compiler.compile([fname], extra_postargs=[flagname])
    except setuptools.distutils.errors.CompileError:
        return False
    finally:
        try:
            os.remove(fname)
        except OSError:
            pass
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14/17] compiler flag.

    The newer version is prefered over c++11 (when it is available).
    """
    #flags = ['-std=c++17', '-std=c++14', '-std=c++11']
    flags = ['-std=c++11']

    for flag in flags:
        if has_flag(compiler, flag):
            return flag

    raise RuntimeError('Unsupported compiler -- at least C++11 support '
                       'is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc', '/DWCHAR_T_IS_16BIT'],
        'unix': [],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == 'unix':
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
            if has_flag(self.compiler, '-Wno-deprecated-declarations'):
                opts.append('-Wno-deprecated-declarations')
            if has_flag(self.compiler, '-Wno-reorder'):
                opts.append('-Wno-reorder')
            if has_flag(self.compiler, '-Wno-unreachable-code'):
                opts.append('-Wno-unreachable-code')

        for ext in self.extensions:
            ext.define_macros = [
                ('VERSION_INFO',
                 '"{}"'.format(self.distribution.get_version()))
            ]
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts
        build_ext.build_extensions(self)

import os.path
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.rst"), encoding='utf-8') as f:
    long_description = f.read()
        
setup(
    name='blahtex',
    version=__version__,
    author='MURAMATSU Atsushi',
    author_email='amura@tomato.sakura.ne.jp',
    url='https://github.com/amuramatsu/blahtex-py',
    description='A python binding of blahtex',
    long_description=long_description,

    keywords='tex latex mathml',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',

        # blahtex is BSD 3-clause license,
        # and my codes are under same license
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        'Topic :: Text Processing :: Markup :: LaTeX',
        'Topic :: Text Processing :: Markup :: XML',
    ],
    
    packages = ['blahtex'],
    ext_modules=ext_modules,
    setup_requires=['pybind11>=2.5.0'],
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)
