#!/usr/bin/env python
from pyhwm2014 import HWM142D, HWM142DPlot

def example14():

    # Longitude vs Height array
    hwm14Obj = HWM142D( altlim=[90., 200.], altstp=1., ap=[-1, 35],
        glonlim=[-90., 90.], glonstp=2., option=4, ut=12., verbose=False )

    # Longitude vs Height plot
    hwm14Gbj = HWM142DPlot( profObj=hwm14Obj, zMin=[-100., -100], zMax=[100., 100.] )

example14()
