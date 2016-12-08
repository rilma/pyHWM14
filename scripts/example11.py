
if __name__ == '__main__':

    def example11():

        from pyhwm2014.pyhwm14 import HWM142D, HWM142DPlot

        # Height vs GMT array
        hwm14Obj = HWM142D( altlim=[90,200], altstp=2, ap=[-1, 35], option=1, 
            utlim=[0.,23.75], utstp=.25, verbose=False )

        # Height vs GMT plot
        hwm14Gbj = HWM142DPlot( profObj=hwm14Obj, zMin=[-75., -100], zMax=[75., 100.] )


    example11()
