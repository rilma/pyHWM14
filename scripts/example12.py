#!/usr/bin/env python
from pyhwm2014 import HWM142D, HWM142DPlot


def example12():
    # Latitude vs Height array
    hwm14Obj = HWM142D(
        altlim=[90.0, 200.0],
        altstp=2.0,
        ap=[-1, 35],
        glatlim=[-90.0, 90.0],
        glatstp=2.0,
        option=2,
        verbose=False,
        ut=12.0,
    )

    # Latitude vs Height plot
    hwm14Gbj = HWM142DPlot(profObj=hwm14Obj, zMin=[-250.0, -100], zMax=[250.0, 100.0])


example12()
