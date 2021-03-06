#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os, stat
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext


# scan the directory for extension files, converting
# them to extension names in dotted notation

def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and path.endswith(".pyx"):
            files.append(path.replace(os.path.sep, ".")[2:-4])
        elif os.path.isdir(path):
            scandir(path, files)
    return files

# generate an Extension object from its dotted name
def makeExtension(extName):
    extPath = extName.replace(".", os.path.sep)+".pyx"
    pxdPath = extName.replace(".", os.path.sep)+".pxd"
    if os.path.isfile(pxdPath):
        flist=[extPath,pxdPath]
    else:
        flist=[extPath]
    return Extension(
        extName,
        flist,
        include_dirs = ["."],   # adding the '.' to include_dirs is CRUCIAL!!
        extra_compile_args = ["-D__LINUX__"],#["-O3", "-Wall","-D__LINUX__","-march=native"],#
        #extra_link_args = ['-g'],
        libraries = ["ueye_api",],
        )

extNames = scandir(".")

# and build up the set of Extension objects
extensions = [makeExtension(name) for name in extNames]


setup(
        #Version del ueye para la que esto funciona
        version ='4.30',
        name =  "pyueye",
        author= 'Ricardo Amezquita Orozco - Ivan Pulido',
        author_email='ramezquitao@cihologramas.com',
        description='Python binding for ueye camera drivers',
        license='BSD',
        url='',
        ext_modules=cythonize(extensions),
        packages=["ueye","wxueye"],
        scripts=['wxVidCap.py'],
        cmdclass = {'build_ext': build_ext},
    )

