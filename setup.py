#!/usr/bin/env python
req = ['nose','numpy','pathlib2',
       'timeutil']
# %%
from setuptools import find_packages
from numpy.distutils.core import Extension, setup
from glob import glob
from os.path import join

name = 'pyhwm2014'

ext = Extension( extra_compile_args=['-w'],
            extra_f90_compile_args=['-w'],
            f2py_options=[ '--quiet' ],
            name='hwm14',
            sources=['source/hwm14.f90']
             )

hwmData1 = glob(join('data', '*.dat'))
hwmData2 = glob(join('data', '*.bin'))
hwmDataFiles = [(join(name, 'data'), hwmData1),
                (join(name, 'data'), hwmData2)]

setup( author=['Ronald Ilma'],
        data_files=hwmDataFiles,
        description='HWM14 neutral winds model',
        ext_modules=[ ext ],
        ext_package=name,
        name=name,
        packages=find_packages(),
        url='https://github.com/rilma/pyHWM14',
        version='1.1.0',
        install_requires=req,
        extras_requires={'plot':['matplotlib','seaborn']},
        dependency_links=[
      'https://github.com/rilma/TimeUtilities/zipball/master#egg=timeutil-999.0'],
        classifiers=[
          'Intended Audience :: Science/Research',
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Topic :: Scientific/Engineering :: Atmospheric Science',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          ],
         python_requires='>=3.10',
)
