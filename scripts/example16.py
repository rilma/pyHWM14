#!/usr/bin/env python
from pyhwm2014 import HWM142D, HWM142DPlot

def example16():

    # Latitude vs Longitude array
    hwm14Obj = HWM142D(alt=130., ap=[-1, 35], glatlim=[-90., 90.], glatstp=1.,
        glonlim=[-180., 180.], glonstp=2., option=6, verbose=False)

    # Latitude vs Longitude plot
    hwm14Gbj = HWM142DPlot( profObj=hwm14Obj, WF=False, zMin=[-150., -150], zMax=[150., 150.] )

example16()
