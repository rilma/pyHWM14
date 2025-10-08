project('pyhwm14', 'c',
  version : '0.1',
  license: 'BSD-3',
  meson_version: '>=0.64.0',
  default_options : ['warning_level=2'],
)

add_languages('fortran')

py_mod = import('python')
py = py_mod.find_installation(pure: false)
py_dep = py.dependency()

incdir_numpy = run_command(py,
  ['-c', 'import os; os.chdir(".."); import numpy; print(numpy.get_include())'],
  check : true
).stdout().strip()

incdir_f2py = run_command(py,
    ['-c', 'import os; os.chdir(".."); import numpy.f2py; print(numpy.f2py.get_include())'],
    check : true
).stdout().strip()

inc_np = include_directories(incdir_numpy, incdir_f2py)

source_dir = 'source/'

hwm14_source = custom_target('hwm14module.c',
  input : [source_dir / 'hwm14.f90'],
  output : ['hwm14module.c', 'hwm14-f2pywrappers.f', 'hwm14-f2pywrappers2.f90'],  # mind the .f90 wrapper!
  command : [py, '-m', 'numpy.f2py', '@INPUT@', '-m', 'hwm14']
)

py.extension_module('hwm14',
  [source_dir / 'hwm14.f90', hwm14_source],
  incdir_f2py / 'fortranobject.c',
  include_directories: inc_np,
  dependencies : py_dep,
  install : true
)
