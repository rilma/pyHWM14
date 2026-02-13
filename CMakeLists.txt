cmake_minimum_required(VERSION 3.15...3.27)
project(pyhwm2014 LANGUAGES Fortran C)

# Find Python
find_package(Python 3.12 COMPONENTS Interpreter Development REQUIRED)

# Get NumPy location
execute_process(
  COMMAND ${Python_EXECUTABLE} -c "import numpy; print(numpy.get_include())"
  OUTPUT_VARIABLE NUMPY_INCLUDE_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

if(NOT NUMPY_INCLUDE_DIR)
  message(FATAL_ERROR "Could not find NumPy")
endif()

# Set f2py command
set(F2PY_EXECUTABLE ${Python_EXECUTABLE} -m numpy.f2py)

# Source files and interface
set(F90_SOURCE ${CMAKE_CURRENT_SOURCE_DIR}/source/hwm14.f90)
set(F2PY_INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/source/reference/hwm14.pyf)
set(PACKAGE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/pyhwm2014)

# Get the extension suffix from Python
execute_process(
  COMMAND ${Python_EXECUTABLE} -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))"
  OUTPUT_VARIABLE EXTENSION_SUFFIX
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

# The extension will be built directly in the pyhwm2014 directory
set(HWM14_EXTENSION ${PACKAGE_DIR}/hwm14${EXTENSION_SUFFIX})

message(STATUS "Python: ${Python_EXECUTABLE}")
message(STATUS "NumPy include: ${NUMPY_INCLUDE_DIR}")
message(STATUS "Extension suffix: ${EXTENSION_SUFFIX}")
message(STATUS "Output location: ${HWM14_EXTENSION}")

# Build the hwm14 extension module using f2py directly in pyhwm2014/
# f2py -c outputs the .so file to the current working directory
add_custom_command(
  OUTPUT ${HWM14_EXTENSION}
  COMMAND ${F2PY_EXECUTABLE}
    -m hwm14
    -c
    ${F2PY_INTERFACE}
    ${F90_SOURCE}
    -I${NUMPY_INCLUDE_DIR}
  WORKING_DIRECTORY ${PACKAGE_DIR}
  DEPENDS ${F2PY_INTERFACE} ${F90_SOURCE}
  COMMENT "Building hwm14 Fortran extension with f2py"
  VERBATIM
)

# Create a target that depends on the extension
add_custom_target(hwm14_ext ALL DEPENDS ${HWM14_EXTENSION})

# Install the generated .so file
file(GLOB_RECURSE HWMSO "${CMAKE_CURRENT_BINARY_DIR}/*.so")
install(FILES ${HWMSO} DESTINATION pyhwm2014 OPTIONAL)

# Install data files
install(FILES
  data/dwm07b104i.dat
  data/gd2qd.dat
  data/hwm123114.bin
  DESTINATION pyhwm2014/data
)
