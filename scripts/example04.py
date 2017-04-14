#!/usr/bin/env python
from pyhwm2014 import HWM14, HWM14Plot

def example04():

    # Single longitudinal profile
    hwm14Obj = HWM14( alt=130., ap=[-1, 35], day=323, glonlim=[-180., 180.], glonstp=2.,
        option=4, verbose=False, year=1993 )

    hwm14Gbj = HWM14Plot( profObj=hwm14Obj )


example04()
