
if __name__ == '__main__':

    def example14():

        from pyhwm2014.pyhwm14 import HWM142D, HWM142DPlot

        # Longitude vs Height array
        hwm14Obj = HWM142D( altlim=[90., 200.], altstp=1., ap=[-1, 35], 
            glonlim=[-90., 90.], glonstp=2., option=4, ut=12., verbose=False )

        # Longitude vs Height plot
        hwm14Gbj = HWM142DPlot( profObj=hwm14Obj )

    example14()
