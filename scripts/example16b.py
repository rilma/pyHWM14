#!/usr/bin/env python
from pyhwm2014 import HWM142D, HWM142DPlot

def example16b():

    # Latitude vs Longitude array
    hwm14Obj = HWM142D(alt=400., ap=[-1, 35], glatlim=[-90., 90.], glatstp=10.,
        glonlim=[-180., 180.], glonstp=20., option=6, verbose=False)

    # Latitude vs Longitude plot (Wind field)
    hwm14Gbj = HWM142DPlot( profObj=hwm14Obj, WF=True, zMin=[-150., -150], zMax=[150., 150.] )

example16b()
