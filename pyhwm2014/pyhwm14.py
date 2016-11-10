
from pyhwm2014 import hwm14
import pylab
#from scipy import append, arange, ones, tile, transpose, reshape
from scipy import append, arange, reshape, transpose


class HWM14:

    def __init__( self, alt=None, altlim=[0., 400.], altstp=25., ap=None, day=None, \
        glat=None, glatlim=[-10.,10.], glatstp=2., glon=None, option=1, stl=None, ut=None, \
        verbose=True, year=None ):

        """ Constructor for the Horizontal Wind Model 14

            Input arguments:
            alt     - altitude in km
            altlim  - altitude range in km
            altstp  - altitude resolution in km
            ap      - 3hr ap index
            day     - day of year (DOY)
            glat    - geog. latitude
            glon    - geog. longitude
            option  - profile selection: 1 (height), 2 (latitude), 3 (local time), 4 (geog. longitude) 
            stl     - solar local time in hr
            ut      - universal time in hr
            verbose - print message to user
            year    - year (YYYY)

            Output:
            The zonal and meridional winds are stored in "self" as follows
            Zonal -> self.Uwind
            Meridional -> self.Vwind

        """

        self.option = option

        if option == 1:     # Height profile
            iday = 150
            if ut is None: ut = 12.
            if glat is None: glat = -45.
            self.glat = glat
            if glon is None: glon = -85.
            self.glon = glon
            if stl is None: stl = 6.3 
            self.stl = stl
            self.altlim = altlim
            self.altstp = altstp
            iap = 80
        elif option == 2:   # Latitude profile
            iday = 305
            if ut is None: ut = 18.
            if alt is None: alt = 250. 
            self.alt = alt
            if glon is None: glon = 30.
            self.glon = glon
            if stl is None: stl = -45.
            self.stl = stl
            self.glatlim = glatlim
            self.glatstp = glatstp
            iap = 48
        elif option == 3:   # Local Time profile
            iday = 75
            if alt is None: alt = 125.
            self.alt = alt
            if glat is None: glat = -45.
            self.glat = glat
            if glon is None: glon = -70.
            self.glon = glon
            iap = 30
        elif option == 4:   # Longitude profile
            iday = 330
            if ut is None: ut = 6.
            self.ut = ut
            if alt is None: alt = 40.
            self.alt = alt
            if glat is None: glat = -45.
            self.glat = glat
            ##self.glon = -70.            
            self.stl = None
            iap = 4
        else: 
            print( 'Invalid option!' )
            return
        
        if ap is None: ap = iap
        if day is None: day = iday
        if year is None: year = 1995

        #if option < 7: 
        self.iyd = int( ( year - 1900 ) * 1e4 ) + day
        if option != 3: self.sec = ut * 3600.
        self.ap = pylab.tile( ap, 2 )
        self.apqt = -pylab.ones( 2 )    # Required for quiet time component         

        self.f107 = 90
        self.f107a = 90
        self.verbose = verbose

        self.Uwind = []
        self.Vwind = []

        if not 'alt' in self.__dict__.keys(): self.HeiProfile()
        elif not 'glat' in self.__dict__.keys(): self.LatProfile()
        elif not 'stl' in self.__dict__.keys(): self.LTProfile()
        elif not 'glon' in self.__dict__.keys(): self.LonProfile()
        else: print( '' )

    #
    # End of '__init__'
    #####


    def HeiProfile( self ):

        """ Height Profile """

        if self.verbose:
            print( 'HEIGHT PROFILE' )
            print( '                 quiet         disturbed             total' )
            print( ' alt      mer      zon      mer      zon      mer      zon' )
         
        self.altbins = pylab.arange( self.altlim[ 0 ], self.altlim[ 1 ] + self.altstp, self.altstp )
        
        for alt in self.altbins:

            wqt = hwm14.hwm14( self.iyd, self.sec, alt, self.glat, self.glon, self.stl, \
                self.f107a, self.f107, self.apqt )

            wdt = hwm14.dwm07( self.iyd, self.sec, alt, self.glat, self.glon, self.ap )

            w = hwm14.hwm14( self.iyd, self.sec, alt, self.glat, self.glon, self.stl, \
                self.f107a, self.f107, self.ap )

            if self.verbose : print( ' %3i %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f' % \
                ( alt, wqt[0], wqt[1], wdt[0], wdt[1], w[0], w[1] ) )
            
            self.Uwind.append( w[ 1 ] )
            self.Vwind.append( w[ 0 ] )
        
    #
    # End of 'HeiProfile'
    #####


    def LatProfile( self ):

        """ Latitude Profile """

        if self.verbose:
            print( 'LATITUDE PROFILE' )
            print( '                   quiet         disturbed             total' )
            print( '  glat      mer      zon      mer      zon      mer      zon' )

        self.glatbins = arange( self.glatlim[0], self.glatlim[1] + self.glatstp, self.glatstp ) 

        for glat in self.glatbins:

            wqt = hwm14.hwm14( self.iyd, self.sec, self.alt, glat, self.glon, self.stl, \
                self.f107a, self.f107, self.apqt )

            wdt = hwm14.dwm07( self.iyd, self.sec, self.alt, glat, self.glon, self.ap )

            w = hwm14.hwm14( self.iyd, self.sec, self.alt, glat, self.glon, self.stl, \
                self.f107a, self.f107, self.ap )

            if self.verbose: print( ' %5.1f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f' % \
                ( glat, wqt[0], wqt[1], wdt[0], wdt[1], w[0], w[1] ) )

            self.Uwind.append( w[ 1 ] )
            self.Vwind.append( w[ 0 ] )

    #
    # End of 'LatProfile'
    #####

    def LTProfile( self ):

        """ Local Time Profile """

        if self.verbose:
            print( 'LOCAL TIME PROFILE' )
            print( '                   quiet         disturbed             total' )
            print( '   stl      mer      zon      mer      zon      mer      zon' )

        self.ltbins = range( 0, 16 + 1 ) 

        for istl in self.ltbins:

            stl = 1.5 * float( istl )
            sec = ( stl - self.glon / 15. ) * 3600.

            wqt = hwm14.hwm14( self.iyd, sec, self.alt, self.glat, self.glon, stl, \
                self.f107a, self.f107, self.apqt )

            wdt = hwm14.dwm07( self.iyd, sec, self.alt, self.glat, self.glon, self.ap )

            w = hwm14.hwm14( self.iyd, sec, self.alt, self.glat, self.glon, stl, \
                self.f107a, self.f107, self.ap )

            if self.verbose: print( ' %5.1f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f' % \
                ( stl, wqt[0], wqt[1], wdt[0], wdt[1], w[0], w[1] ) )

            self.Uwind.append( w[ 1 ] )
            self.Vwind.append( w[ 0 ] )

    #
    # End of 'LTProfile'
    #####

    def LonProfile( self ):

        """ Longitude Profile """

        if self.verbose:
            print( 'LONGITUDE PROFILE' )
            print( '                   quiet         disturbed             total' )
            print( '  glon      mer      zon      mer      zon      mer      zon' )

        self.glonbins = range( -180, 180 + 20, 20 )

        for glon in self.glonbins:

            stl = self.ut + glon / 15.

            wqt = hwm14.hwm14( self.iyd, self.sec, self.alt, self.glat, glon, stl, \
                self.f107a, self.f107, self.apqt )

            wdt = hwm14.dwm07( self.iyd, self.sec, self.alt, self.glat, glon, self.ap )

            w = hwm14.hwm14( self.iyd, self.sec, self.alt, self.glat, glon, stl, \
                self.f107a, self.f107, self.ap )

            if self.verbose: print( ' %5.1f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f' % \
                ( glon, wqt[0], wqt[1], wdt[0], wdt[1], w[0], w[1] ) )

            self.Uwind.append( w[ 1 ] )
            self.Vwind.append( w[ 0 ] )

    #
    # End of 'LonProfile'
    #####

#
# End of HWM14
######


class HWM14Plot:

    def __init__( self, profObj=None ):

        """
            Constructor of class resposible of graphical reports for the 
            Horizontal Wind Model 14. It requires the methods (instance) 
            returned by class "HWM14"
        """    

        if profObj != None:
            self.option = profObj.option
            if self.option >= 1 and self.option <= 4:
                self.Uwind = profObj.Uwind
                self.Vwind = profObj.Vwind                
            valid = True
            if self.option == 1:
                self.altbins = profObj.altbins
                self.HeiProfPlot()
            elif self.option == 2:
                self.glatbins = profObj.glatbins 
                self.LatProfPlot()
            elif self.option == 3:
                self.ltbins = profObj.ltbins 
                self.LTProfPlot()
            elif self.option == 4:
                self.glonbins = profObj.glonbins
                self.LonProfPlot()
            else: 
                print( 'Invalid option!' )
                valid = False
            if valid: 
                pylab.show()
        else:
            print( 'Wrong inputs!' )

    #
    # End of '__init__'
    #####

    def HeiProfPlot( self ):

        pylab.plot( self.Uwind, self.altbins, label='U' )
        pylab.plot( self.Vwind, self.altbins, label='V' )
        pylab.xlabel( r'(m/s)' );
        pylab.ylabel( r'(km)')
        pylab.legend( loc='best' )        

    #
    # End of 'HeiProfPlot' 
    #####

    def LatProfPlot( self ):

        pylab.plot( self.glatbins, self.Uwind, label='U' )
        pylab.plot( self.glatbins, self.Vwind, label='V' )
        pylab.xlabel( r'Geog. Lat. ($^\circ$)' );
        pylab.ylabel( r'(m/s)')
        pylab.legend( loc='best' )        

    #
    # End of 'LatProfPlot' 
    #####

    def LTProfPlot( self ):

        pylab.plot( self.ltbins, self.Uwind, label='U' )
        pylab.plot( self.ltbins, self.Vwind, label='V' )
        pylab.xlabel( r'(LT)' );
        pylab.ylabel( r'(m/s)')
        pylab.legend( loc='best' )        

    #
    # End of 'LTProfPlot' 
    #####

    def LonProfPlot( self ):

        pylab.plot( self.glonbins, self.Uwind, label='U' )
        pylab.plot( self.glonbins, self.Vwind, label='V' )
        pylab.xlabel( r'Geog. Lon. ($^\circ$)' );
        pylab.ylabel( r'(m/s)')
        pylab.legend( loc='best' )        

    #
    # End of 'LonProfPlot' 
    #####

#
# End of 'HWM14Plot' 
#####


class HWM142D:
    
    def __init__( self, alt=None, altlim=[0., 400.], altstp=25., ap=None, day=None, 
        glat=None, glatlim=[-40., 40.], glatstp=5., glon=None, option=1, stl=None, sltlim=[0., 24.], sltstp=1., 
        ut=None, verbose=True, year=None ):    

        """
        """

        self.option = option

        if option == 1:     # Time vs Height
            iday = 150
            if ut is None: ut = 12.
            if glat is None: glat = -45.
            self.glat = glat
            if glon is None: glon = -85.
            self.glon = glon
            if stl is None: stl = 6.3 
            self.stl = stl
            self.sltlim = sltlim
            self.sltstp = sltstp
            self.altlim = altlim            
            self.altstp = altstp
            iap = 80
        elif option == 2:   # Latitude vs Height`
            iday = 305
            if ut is None: ut = 18.
            if alt is None: alt = 250. 
            self.alt = alt
            if glon is None: glon = 30.
            self.glon = glon
            if stl is None: stl = -45.
            self.stl = stl
            self.altlim = altlim
            self.altstp = altstp
            self.glatlim = glatlim
            self.glatstp = glatstp
            iap = 48            
        else: 
            print( 'Invalid option!' )
            return
        
        if ap is None: ap = iap
        if day is None: day = iday
        if year is None: year = 1995
 
        self.iyd = int( ( year - 1900 ) * 1e4 ) + day
        if option != 3: self.sec = ut * 3600.
        self.ap = pylab.tile( ap, 2 )
        self.apqt = -pylab.ones( 2 )    # Required for quiet time component         

        self.f107 = 90
        self.f107a = 90
        self.verbose = verbose

        self.Uwind = []
        self.Vwind = []

        if not 'alt' in self.__dict__.keys(): self.HeiVsLTArray()
        elif not 'glat' in self.__dict__.keys(): self.LatProfile()
        #elif not 'stl' in self.__dict__.keys(): self.LTProfile()
        #elif not 'glon' in self.__dict__.keys(): self.LonProfile()
        else: print( '' )

    #
    # End of '__init__'
    #####

    def HeiVsLTArray( self ):

        """
        """


        self.sltbins = pylab.arange( self.sltlim[ 0 ], self.sltlim[ 1 ] + self.sltstp, self.sltstp )

        for slt in self.sltbins:
            
            ut = slt - self.glon / 15.

            # Generates model data
            hwm14Obj = HWM14( altlim=self.altlim, altstp=self.altstp, ap=None, 
                glat=self.glat, glon=self.glon, option=self.option, ut=ut, \
                verbose=self.verbose )

            Uwind = pylab.reshape( hwm14Obj.Uwind, ( len( hwm14Obj.Uwind ), 1 ) )
            Vwind = pylab.reshape( hwm14Obj.Vwind, ( len( hwm14Obj.Vwind ), 1 ) )
            self.Uwind = Uwind if slt == self.sltlim[ 0 ] else pylab.append( self.Uwind, Uwind, axis=1 )
            self.Vwind = Vwind if slt == self.sltlim[ 0 ] else pylab.append( self.Vwind, Vwind, axis=1 )

        self.altbins = hwm14Obj.altbins


    def LatProfile(self):

        """        """

        self.altbins = arange(self.altlim[0], self.altlim[1] + self.altstp, self.altstp)

        for _alt in self.altbins:

            hwm14Obj = HWM14( alt=_alt, ap=None, glatlim=self.glatlim, glatstp=self.glatstp, 
                glon=self.glon, option=self.option, verbose=self.verbose )

            Uwind = reshape( hwm14Obj.Uwind, ( len( hwm14Obj.Uwind ), 1 ) )
            Vwind = reshape( hwm14Obj.Vwind, ( len( hwm14Obj.Vwind ), 1 ) )
            self.Uwind = Uwind if _alt == self.altlim[ 0 ] else append( self.Uwind, Uwind, axis=1 )
            self.Vwind = Vwind if _alt == self.altlim[ 0 ] else append( self.Vwind, Vwind, axis=1 )

        self.glatbins = hwm14Obj.glatbins

        self.Uwind = transpose(self.Uwind)
        self.Vwind = transpose(self.Vwind)

#
# End of 'HWM142D'
#####


class HWM142DPlot:

    def __init__( self, profObj=None ):

        """
            Constructor of class resposible of graphical reports for the 
            Horizontal Wind Model 14. It requires the methods (instance) 
            returned by class "HWM14"
        """    

        if profObj != None:
            self.option = profObj.option
            if self.option >= 1 and self.option <= 4:
                self.Uwind = profObj.Uwind
                self.Vwind = profObj.Vwind                
            valid = True
            if self.option == 1:
                self.altbins = profObj.altbins
                self.altlim = profObj.altlim
                self.sltbins = profObj.sltbins
                self.sltlim = profObj.sltlim
                self.HeiVsLTPlot()
            elif self.option == 2:
                self.glatbins = profObj.glatbins
                self.glatlim = profObj.glatlim
                self.altbins = profObj.altbins
                self.altlim = profObj.altlim 
                self.LatVsHeiPlot()
            # elif self.option == 3:
            #     self.ltbins = profObj.ltbins 
            #     self.LTProfPlot()
            # elif self.option == 4:
            #     self.glonbins = profObj.glonbins
            #     self.LonProfPlot()
            else: 
                print( 'Invalid option!' )
                valid = False
            if valid: 
                pylab.show()
        else:
            print( 'Wrong inputs!' )

    #
    # End of '__init__'
    #####


    def XVsY2DPlot( self, ax, xVal, yVal, zVal, cmap=None, title=None, 
        xlabel=None, xlim=None, ylabel=None, ylim=None, zlabel=None, zMax=None, zMin=None ):

        X, Y = pylab.meshgrid( xVal, yVal )
        X = pylab.transpose( X )
        Y = pylab.transpose( Y )

        C = pylab.transpose( zVal )
        ipn = ax.pcolor( X, Y, C, cmap=cmap, edgecolors='None', norm=pylab.Normalize(), vmax=zMax, vmin=zMin )
        ax.set_xlim( xlim )
        ax.set_ylim( ylim )
        ax.set_title( title )
        ax.set_xlabel( xlabel )
        ax.set_ylabel( ylabel )

        cbpn = pylab.colorbar( ipn )
        cbpn.set_label( zlabel )        

    #
    # End of 'XVsY2DPlot' 
    #####


    def HeiVsLTPlot( self ):

        fig = pylab.figure( figsize=(15,6) )

        ax = pylab.subplot(121)                
        cmap = pylab.cm.RdBu_r
        self.XVsY2DPlot( ax, self.sltbins, self.altbins, self.Uwind, cmap=cmap, title=r'Zonal wind (U)',
            xlabel=r'(hour)', xlim=self.sltlim, ylabel=r'(km)', ylim=self.altlim, zlabel=r'm/s', zMax=None, zMin=None )
                
        ax = pylab.subplot(122)

        self.XVsY2DPlot( ax, self.sltbins, self.altbins, self.Vwind, cmap=cmap, title=r'Meridional wind (V)',
            xlabel=r'(hour)', xlim=self.sltlim, ylabel=r'(km)', ylim=self.altlim, zlabel=r'm/s', zMax=None, zMin=None )

    #
    # End of 'HeiProfPlot' 
    #####


    def LatVsHeiPlot(self):

        fig = pylab.figure( figsize=(15,6) )

        ax = pylab.subplot(121)                
        cmap = pylab.cm.RdBu_r
        self.XVsY2DPlot( ax, self.glatbins, self.altbins, self.Uwind, cmap=cmap, title=r'Zonal wind (U)',
            xlabel=r'Geog. Lat. ($^o$)', xlim=self.glatlim, ylabel=r'(km)', ylim=self.altlim, zlabel=r'm/s', zMax=None, zMin=None )
                
        ax = pylab.subplot(122)

        self.XVsY2DPlot( ax, self.glatbins, self.altbins, self.Vwind, cmap=cmap, title=r'Meridional wind (V)',
            xlabel=r'Geog. Lat. ($^o$)', xlim=self.glatlim, ylabel=r'(km)', ylim=self.altlim, zlabel=r'm/s', zMax=None, zMin=None )

    #
    # End of 'HeiProfPlot' 
    #####    

#
# End of 'HWM14Plot' 
#####


if __name__ == '__main__':


    def main():

        """ Example """

        # Generates model data
        hwm14Obj = HWM14( altlim=[0, 200], altstp=5., glat=-12., glon=283.13, option=4, verbose=False )
        
        # Produces simple graphical report
        hwm14Gbj = HWM14Plot( profObj=hwm14Obj )

    #
    # End of 'main'
    #####


    main()

#
# End of '__if__'
#####