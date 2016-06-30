import codecs
import os
import re

from setuptools import setup, find_packages

import sys
from cx_Freeze import setup, Executable

import scipy
includefiles_list=[]
scipy_path = os.path.dirname(scipy.__file__)
includefiles_list.append(scipy_path)

###################################################################

NAME = "omsim"
PACKAGES = find_packages(where="")
META_PATH = "__init__.py"
KEYWORDS = ["optical maps"]
CLASSIFIERS = [
        "Development Status :: 0 - Unstable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GPL2 License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
]
INSTALL_REQUIRES = ["scipy"]

###################################################################

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
        """
        Build an absolute path from *parts* and and return the contents of the
        resulting file.  Assume UTF-8 encoding.
        """
        with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
                return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
        """
        Extract __*meta*__ from META_FILE.
        """
        meta_match = re.search(
                r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
                META_FILE, re.M
        )
        if meta_match:
                return meta_match.group(1)
        raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


base = 'Console'
if sys.platform == 'win32':
        base = 'Win32GUI'

options = {
        'build_exe': {
                'include_files': includefiles_list,
                'optimize': '2'
    }
}

executables = [
        Executable('__main__.py', base=base)
]

if __name__ == "__main__":
        setup(
                name=NAME,
                description=find_meta("description"),
                license=find_meta("license"),
                url=find_meta("uri"),
                version=find_meta("version"),
                author=find_meta("author"),
#                author_email=find_meta("email"),
                maintainer=find_meta("author"),
#                maintainer_email=find_meta("email"),
                keywords=KEYWORDS,
                long_description=read("README.rst"),
                packages=PACKAGES,
                package_dir={"": ".."},
                zip_safe=False,
                classifiers=CLASSIFIERS,
                install_requires=INSTALL_REQUIRES,
                executables=executables,
                options=options
        )
