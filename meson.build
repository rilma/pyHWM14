project('pyhwm2014', 'fortran',
  version: '1.1.0',
  meson_version: '>=0.63.0'
)

# Find Python and NumPy
py_mod = import('python')
py = py_mod.find_installation()
py_dep = py.dependency(embed: true)

# Find NumPy
numpy_inc = run_command(
  py,
  '-c',
  'import numpy; print(numpy.get_include())',
  check: true
).stdout().strip()

# Fortran compiler settings
fc = meson.get_compiler('fortran')

# Build f2py extension
f2py = py_mod.find_installation().get_path('scripts') / 'f2py'

# Compile Fortran source to extension module
hwm14_f90_src = 'source/hwm14.f90'

# Create f2py signature file if it exists (optional)
# For now, we'll use direct f2py compilation
executable(
  'gen_hwm14',
  hwm14_f90_src,
  fortran_args: ['-w'],
  install: false,
)

# Install Python package
subdir('pyhwm2014')
