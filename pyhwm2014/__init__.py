
from os import environ
from os.path import dirname, join, realpath

# Defines a shell variable 'HWMPATH' which indicates the location of
# 'hwm123114.bin', 'dwm07b104i.dat', and 'gd2qd.dat'
#
environ['HWMPATH'] = join(dirname(realpath(__file__)), 'data')
