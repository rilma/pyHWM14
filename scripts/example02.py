if __name__ == '__main__':

    def example02():

        from pyhwm2014.pyhwm14 import HWM14, HWM14Plot

        # Single latitudinal profile
        hwm14Obj = HWM14( alt=130., ap=[-1, 35], day=323, glatlim=[-90.,90.],
            glatstp=1., option=2, ut=11.66667, verbose=False, year=1993 )
            
        hwm14Gbj = HWM14Plot( profObj=hwm14Obj )


    example02()