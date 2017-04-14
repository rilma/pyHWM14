#!/usr/bin/env python
from pyhwm2014 import HWM14, HWM14Plot

def example02():

    # Single latitudinal profile
    hwm14Obj = HWM14( alt=130., ap=[-1, 35], day=323, glatlim=[-90.,90.],
        glatstp=1., option=2, ut=11.66667, verbose=False, year=1993 )

    # Latitudinal profile plot
    hwm14Gbj = HWM14Plot( profObj=hwm14Obj )

example02()
