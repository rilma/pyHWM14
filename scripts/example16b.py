#!/usr/bin/env python
from pyhwm2014 import HWM142D, HWM142DPlot


def example16b():
    # Latitude vs Longitude array
    hwm14Obj = HWM142D(
        alt=400.0,
        ap=[-1, 35],
        glatlim=[-90.0, 90.0],
        glatstp=10.0,
        glonlim=[-180.0, 180.0],
        glonstp=20.0,
        option=6,
        verbose=False,
    )

    # Latitude vs Longitude plot (Wind field)
    hwm14Gbj = HWM142DPlot(profObj=hwm14Obj, WF=True, zMin=[-150.0, -150], zMax=[150.0, 150.0])


example16b()
