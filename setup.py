#!/usr/bin/env python
import setuptools
from glob import glob
from os.path import join
from numpy.distutils.core import Extension, setup

name = 'pyhwm2014'

ext = Extension( extra_compile_args=['-w'],
            extra_f90_compile_args=['-w'],
            f2py_options=[ '--quiet' ], 
            name='hwm14', 
            sources=['source/hwm14.pyf', 'source/hwm14.f90']
             )

hwmData1 = glob(join('data', '*.dat'))
hwmData2 = glob(join('data', '*.bin'))
hwmDataFiles = [(join(name, 'data'), hwmData1), 
                (join(name, 'data'), hwmData2)]

if __name__ == '__main__':

    setup( author='Ronald Ilma', 
        author_email='rri5@cornell.edu',
        data_files=hwmDataFiles, 
        description='HWM14 neutral winds model', 
        ext_modules=[ ext ],
        ext_package=name, 
        name=name, 
        packages=[name],  
        url='https://github.com/rilma/pyHWM14', 
        version='0.0.2',
        )
