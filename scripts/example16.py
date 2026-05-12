#!/usr/bin/env python
from pyhwm2014 import HWM142D, HWM142DPlot


def example16():
    # Latitude vs Longitude array
    hwm14Obj = HWM142D(
        alt=130.0,
        ap=[-1, 35],
        glatlim=[-90.0, 90.0],
        glatstp=1.0,
        glonlim=[-180.0, 180.0],
        glonstp=2.0,
        option=6,
        verbose=False,
    )

    # Latitude vs Longitude plot
    hwm14Gbj = HWM142DPlot(profObj=hwm14Obj, WF=False, zMin=[-150.0, -150], zMax=[150.0, 150.0])


example16()
