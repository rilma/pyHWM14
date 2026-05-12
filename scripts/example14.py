#!/usr/bin/env python
from pyhwm2014 import HWM142D, HWM142DPlot


def example14():
    # Longitude vs Height array
    hwm14Obj = HWM142D(
        altlim=[90.0, 200.0],
        altstp=1.0,
        ap=[-1, 35],
        glonlim=[-90.0, 90.0],
        glonstp=2.0,
        option=4,
        ut=12.0,
        verbose=False,
    )

    # Longitude vs Height plot
    hwm14Gbj = HWM142DPlot(profObj=hwm14Obj, zMin=[-100.0, -100], zMax=[100.0, 100.0])


example14()
