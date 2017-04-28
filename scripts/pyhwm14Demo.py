#!/usr/bin/env python
from pyhwm2014 import hwm14

ut, stl, glon, alt, glat, f107a, f107, ap = 12, 17, -77.76, 130., -11.95, 90, 90, [2,2]
iyd = 95150
sec = ut * 3600.
sec = ( stl - glon / 15. ) * 3600.
w = hwm14.hwm14( iyd, sec, alt, glat, glon, stl, f107a, f107, ap )
print(w)

#############################################################################################################

# from pyhwm2014.pyhwm14 import HWM14, HWM14Plot

# # Single Height profile
# #hwm14Obj = HWM14( option=1, ut=12, verbose=False )
# hwm14Obj = HWM14( altlim=[50,200], altstp=10, option=1, ut=5, verbose=False )
# hwm14Gbj = HWM14Plot( profObj=hwm14Obj )

#############################################################################################################

# from pyhwm2014.pyhwm14 import HWM142D, HWM142DPlot

# # # Height vs LT array
# # hwm14Obj = HWM142D( altlim=[90,200], altstp=2, option=1, sltlim=[0.,23.75], sltstp=.25, verbose=False )
# # hwm14Gbj = HWM142DPlot( profObj=hwm14Obj )

# Latitude vs Height array
# hwm14Obj = HWM142D( altlim=[90., 200.], altstp=10., glatlim=[-40., 40.], glatstp=5., 
#     option=2, verbose=False )
# Latitude vs Height plot
# hwm14Gbj = HWM142DPlot( profObj=hwm14Obj )

#############################################################################################################
#############################################################################################################


# Examples at README.rst
#

# #############################################################################################################

# from pyhwm2014.pyhwm14 import HWM14, HWM14Plot

# hwm14Obj = HWM14( option=1, verbose=False )
# hwm14Gbj = HWM14Plot( profObj=hwm14Obj )

# #############################################################################################################

# from pyhwm2014.pyhwm14 import HWM14

# hwm14Obj = HWM14( option=1, verbose=True )

# #############################################################################################################

# from pyhwm2014.pyhwm14 import HWM14, HWM14Plot
# hwm14Obj = HWM14( option=2, verbose=False )
# hwm14Gbj = HWM14Plot( profObj=hwm14Obj )

# #############################################################################################################

# from pyhwm2014.pyhwm14 import HWM14, HWM14Plot
# hwm14Obj = HWM14( option=3, verbose=False )
# hwm14Gbj = HWM14Plot( profObj=hwm14Obj )

# #############################################################################################################

# from pyhwm2014.pyhwm14 import HWM14, HWM14Plot
# hwm14Obj = HWM14( option=4, verbose=False )
# hwm14Gbj = HWM14Plot( profObj=hwm14Obj )

# #############################################################################################################
