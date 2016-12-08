
if __name__ == '__main__':

    def example12():

        from pyhwm2014.pyhwm14 import HWM142D, HWM142DPlot

        # Latitude vs Height array
        hwm14Obj = HWM142D( altlim=[90., 200.], altstp=2., ap=[-1, 35], 
            glatlim=[-90., 90.], glatstp=2., option=2, verbose=False, ut=12. )

        # Latitude vs Height plot
        hwm14Gbj = HWM142DPlot( profObj=hwm14Obj, zMin=[-250., -100], zMax=[250., 100.] )


    example12()
