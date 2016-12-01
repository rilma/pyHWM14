
import seaborn
from pyhwm2014 import hwm14
import pylab
from scipy import append, arange, floor, ones, reshape, tile, transpose


class HWM14:

    def __init__( self, alt=300., altlim=[0., 400.], altstp=25., ap=[-1, 35],
        f107=-1., f107a=-1., day=323, glat=-11.95, glatlim=[-10.,10.],
        glatstp=2., glon=-76.77, glonlim=[-20., 20.], glonstp=2., option=1, 
        stl=-1, ut=12., utlim=[0., 23.], utstp=1., verbose=True, year=1993 ):

        """ Constructor for the Horizontal Wind Model 14

            Input arguments:
            alt     - altitude in km
            altlim  - altitude range in km
            altstp  - altitude resolution in km
            ap      - 2-element list with
                        ap[0] -> not used
                        ap[1] -> 3hr ap index
            day     - day of year (DOY)
            glat    - geog. latitude
            glon    - geog. longitude
            f107a   - not used
            f107    - not used
            option  - profile selection:
                        1 (height)
                        2 (latitude)
                        3 (local time)
                        4 (geog. longitude)
            stl     - solar local time in hr (not used)
            ut      - universal time in hr
            verbose - print message to user
            year    - year (YYYY)

            Output:
            The zonal and meridional winds are stored in "self" as follows
            Zonal -> self.Uwind
            Meridional -> self.Vwind

        """

        self.option = option
        self.year, self.doy = year, day


        if option == 1:     # Height profile
            self.glat = glat
            self.glon = glon
            self.stl = stl
            self.altlim = altlim
            self.altstp = altstp
        elif option == 2:   # Latitude profile
            self.alt = alt
            self.glon = glon
            self.stl = stl
            self.glatlim = glatlim
            self.glatstp = glatstp
        elif option == 3:   # Local Time profile
            self.alt = alt
            self.glat = glat
            self.glon = glon
            self.utlim = utlim
            self.utstp = utstp
        elif option == 4:   # Longitude profile
            self.ut = ut
            self.alt = alt
            self.glat = glat
            self.glonlim = glonlim
            self.glonstp = glonstp
            self.stl = stl
        else:
            print( 'Invalid option!' )
            return
        
        self.iyd = int((year - (2000 if year > 1999 else 1900)) * 10000) + day

        if option != 3: 
            self.sec = ut * 3600.
            self.stl = stl
            self.ut = ut

        self.ap = ap
        self.apqt = -ones(2)    # Required for quiet time component

        self.f107 = f107
        self.f107a = f107a
        self.verbose = verbose

        self.Uwind = []
        self.Vwind = []

        if not 'alt' in self.__dict__.keys(): self.HeiProfile()
        elif not 'glat' in self.__dict__.keys(): self.LatProfile()
        elif not 'ut' in self.__dict__.keys(): self.GMTProfile()
        elif not 'glon' in self.__dict__.keys(): self.LonProfile()
        else: print('')

    #
    # End of '__init__'
    #####


    def HeiProfile( self ):

        """ Height Profile """

        if self.verbose:
            print( 'HEIGHT PROFILE' )
            print( '                 quiet         disturbed             total' )
            print( ' alt      mer      zon      mer      zon      mer      zon' )

        self.altbins = arange( self.altlim[ 0 ], self.altlim[ 1 ] + self.altstp, self.altstp )

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

    def GMTProfile( self ):

        """ GMT Profile """

        if self.verbose:
            print( 'GMT PROFILE' )
            print( '                   quiet         disturbed             total' )
            print( '   stl      mer      zon      mer      zon      mer      zon' )

        self.utbins = arange(self.utlim[0], self.utlim[1] + self.utstp, self.utstp)
                
        for ut in self.utbins:
        
            sec = ut * 3600

            wqt = hwm14.hwm14( self.iyd, sec, self.alt, self.glat, self.glon, -1, \
                self.f107a, self.f107, self.apqt )

            wdt = hwm14.dwm07( self.iyd, sec, self.alt, self.glat, self.glon, self.ap )

            w = hwm14.hwm14( self.iyd, sec, self.alt, self.glat, self.glon, -1, \
                self.f107a, self.f107, self.ap )

            if self.verbose: print( ' %5.1f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f' % \
                ( ut, wqt[0], wqt[1], wdt[0], wdt[1], w[0], w[1] ) )

            self.Uwind.append( w[ 1 ] )
            self.Vwind.append( w[ 0 ] )

    #
    # End of 'GMTProfile'
    #####

    def LonProfile( self ):

        """ Longitude Profile """

        if self.verbose:
            print( 'LONGITUDE PROFILE' )
            print( '                   quiet         disturbed             total' )
            print( '  glon      mer      zon      mer      zon      mer      zon' )

        self.glonbins = arange(self.glonlim[0], self.glonlim[1] + self.glonstp, self.glonstp)

        for glon in self.glonbins:

            wqt = hwm14.hwm14( self.iyd, self.sec, self.alt, self.glat, glon, -1, \
                self.f107a, self.f107, self.apqt )

            wdt = hwm14.dwm07( self.iyd, self.sec, self.alt, self.glat, glon, self.ap )

            w = hwm14.hwm14( self.iyd, self.sec, self.alt, self.glat, glon, -1, \
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

            self.year, self.doy = profObj.year, profObj.doy
            if self.option != 3: self.ut = profObj.ut
            if self.option != 2: self.glat = profObj.glat
            if self.option != 4: self.glon = profObj.glon
            if self.option != 1: self.alt = profObj.alt
            self.ap = profObj.ap

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
                self.utbins = profObj.utbins
                self.GMTProfPlot()
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

    def GetHHMMSS(self):
        hh = floor(self.ut)
        dummy = self.ut - hh
        mm = floor(dummy * 60)
        dummy = dummy * 60 - mm
        self.second = int(floor(dummy * 60))
        self.hour, self.minute = int(hh), int(mm)
    #
    # End of 'GetHHMMSS'
    #####

    def GetTitle(self):

        dateStr = 'DATE: {:4d}.{:03d}'.format(self.year, self.doy)

        try:
            self.GetHHMMSS()
            timeStr = 'TIME: {:02d}:{:02d} UT'.format(self.hour, self.minute)
        except:
            pass

        apStr = 'ap: {:3d}'.format(self.ap[1])

        try:
            altStr = 'ALT: {:7.2f} km'.format(self.alt)
        except:
            pass

        try:
            latStr = '{:6.2f}$^\circ${:s}'.format(abs(self.glat),
                'N' if self.glat > 0 else 'S')
        except:
            pass

        try:
            lonStr = '{:6.2f}$^\circ${:s}'.format(abs(self.glon),
                'E' if self.glon > 0 else 'W')
        except:
            pass

        try:
            locStr = '{:s}, {:s}'.format(latStr, lonStr)
        except:
            pass

        if self.option == 1:
            self.title = '{:s} - {:s} - {:s} - {:s}'.format(dateStr, timeStr, apStr, locStr)
        elif self.option == 2:
            self.title = '{:s} - {:s} - {:s} - {:s} - GEOG. LON.: {:s}'.format(dateStr, timeStr, apStr, altStr, lonStr)
        elif self.option == 3:
            self.title = '{:s} - {:s} - {:s} - {:s}'.format(dateStr, apStr, altStr, locStr)
        elif self.option == 4:
            self.title = '{:s} - {:s} - {:s} - {:s} - GEOG. LAT.: {:s}'.format(dateStr, timeStr, apStr, altStr, latStr)

    #
    # End of 'GetTitle'
    #####

    def HeiProfPlot( self ):

        self.GetTitle()

        pylab.plot( self.Uwind, self.altbins, label='U' )
        pylab.plot( self.Vwind, self.altbins, label='V' )
        pylab.ylim(self.altbins[[0, -1]])
        pylab.title(self.title)
        pylab.xlabel( r'(m/s)' );
        pylab.ylabel( r'(km)')
        pylab.legend( loc='best' )

    #
    # End of 'HeiProfPlot'
    #####

    def LatProfPlot( self ):

        self.GetTitle()

        pylab.plot( self.glatbins, self.Uwind, label='U' )
        pylab.plot( self.glatbins, self.Vwind, label='V' )
        pylab.xlim(self.glatbins[[0, -1]])
        pylab.title(self.title)        
        pylab.xlabel( r'Geog. Lat. ($^\circ$)' );
        pylab.ylabel( r'Wind speed (m/s)')
        pylab.legend( loc='best' )

    #
    # End of 'LatProfPlot'
    #####

    def GMTProfPlot( self ):

        self.GetTitle()

        pylab.plot( self.utbins, self.Uwind, label='U' )
        pylab.plot( self.utbins, self.Vwind, label='V' )
        pylab.xlim(self.utbins[[0, -1]])
        pylab.title(self.title)
        pylab.xlabel( r'Hour (GMT)' )
        pylab.ylabel( r'Wind speed (m/s)')
        pylab.legend( loc='best' )

    #
    # End of 'GMTProfPlot'
    #####

    def LonProfPlot( self ):

        self.GetTitle()

        pylab.plot( self.glonbins, self.Uwind, label='U' )
        pylab.plot( self.glonbins, self.Vwind, label='V' )
        pylab.xlim(self.glonbins[[0, -1]])
        pylab.title(self.title)
        pylab.xlabel( r'Geog. Lon. ($^\circ$)' );
        pylab.ylabel( r'Wind speed (m/s)')
        pylab.legend( loc='best' )

    #
    # End of 'LonProfPlot'
    #####

#
# End of 'HWM14Plot'
#####


class HWM142D:

    def __init__( self, alt=300., altlim=[0., 400.], altstp=25., ap=[-1, 35],
        day=323, f107=-1, f107a=-1, glat=-11.95, glatlim=[-40., 40.],
        glatstp=5., glon=-76.77, glonlim=[-40., 40], glonstp=5., option=1, 
        stl=-1, utlim=[0., 24.], utstp=1., ut=12., verbose=True, year=1993 ):

        """
        """

        self.option = option
        self.year, self.doy = year, day
        if not option in [3, 5]: self.ut = ut

        if option == 1:     # Time vs Height
            self.glat = glat
            self.glon = glon
            self.stl = stl
            self.utlim = utlim
            self.utstp = utstp
            self.altlim = altlim
            self.altstp = altstp
        elif option == 2:   # Latitude vs Height
            self.alt = alt
            self.glon = glon
            self.stl = stl
            self.altlim = altlim
            self.altstp = altstp
            self.glatlim = glatlim
            self.glatstp = glatstp
        elif option == 3:   # GMT vs Latitude
            self.alt = alt
            self.glon = glon
            self.glatlim = glatlim
            self.glatstp = glatstp
            self.utlim = utlim
            self.utstp = utstp            
        elif option == 4:   # Longitude vs Height
            self.alt = alt
            self.glat = glat
            self.altlim = altlim
            self.altstp = altstp
            self.glonlim = glonlim
            self.glonstp = glonstp
        elif option == 5:   # GMT vs Longitude
            self.alt = alt
            self.glon = glon
            self.glonlim = glonlim
            self.glonstp = glonstp            
            self.utlim = utlim
            self.utstp = utstp
        elif option == 6:   # Longitude vs Latitude
            self.alt = alt
            self.glatlim = glatlim
            self.glatstp = glatstp
            self.glonlim = glonlim
            self.glonstp = glonstp
        else:
            print( 'Invalid option!' )
            return

        self.iyd = int((year - (2000 if year > 1999 else 1900)) * 10000) + day
        if option != 3: self.sec = ut * 3600.
        self.ap = ap
        self.apqt = -ones( 2 )    # Required for quiet time component

        self.f107 = f107
        self.f107a = f107a
        self.verbose = verbose

        self.Uwind = []
        self.Vwind = []

        if not 'alt' in self.__dict__.keys(): self.HeiVsLTArray()
        elif not 'glat' in self.__dict__.keys() and not 'glon' in self.__dict__.keys(): self.LonVsLatArray()
        elif not 'glat' in self.__dict__.keys() and not 'ut' in self.__dict__.keys(): self.LatVsGMTArray()
        elif not 'glat' in self.__dict__.keys(): self.LatVsHeiArray()        
        elif not 'glon' in self.__dict__.keys(): self.LonVsHeiArray()
        else: print( '' )

    #
    # End of '__init__'
    #####

    def HeiVsLTArray( self ):

        """
        """

        self.utbins = arange( self.utlim[ 0 ], self.utlim[ 1 ] + self.utstp, self.utstp )

        for ut in self.utbins:

            # Generates model data
            hwm14Obj = HWM14( altlim=self.altlim, altstp=self.altstp, ap=self.ap,
                glat=self.glat, glon=self.glon, option=self.option, ut=ut, \
                verbose=self.verbose )

            Uwind = reshape( hwm14Obj.Uwind, ( len( hwm14Obj.Uwind ), 1 ) )
            Vwind = reshape( hwm14Obj.Vwind, ( len( hwm14Obj.Vwind ), 1 ) )
            self.Uwind = Uwind if ut == self.utlim[ 0 ] else append( self.Uwind, Uwind, axis=1 )
            self.Vwind = Vwind if ut == self.utlim[ 0 ] else append( self.Vwind, Vwind, axis=1 )

        self.altbins = hwm14Obj.altbins

    #
    # End of 'HeiVsLTArray'
    #####

    def LatVsHeiArray(self):

        """        """

        self.altbins = arange(self.altlim[0], self.altlim[1] + self.altstp, self.altstp)

        for _alt in self.altbins:

            if True:

                hwm14Obj = HWM14( alt=_alt, ap=self.ap, glatlim=self.glatlim, 
                    glatstp=self.glatstp, glon=self.glon, option=self.option, 
                    verbose=self.verbose, ut=self.ut )

            else:

                pass

            Uwind = reshape( hwm14Obj.Uwind, ( len( hwm14Obj.Uwind ), 1 ) )
            Vwind = reshape( hwm14Obj.Vwind, ( len( hwm14Obj.Vwind ), 1 ) )
            self.Uwind = Uwind if _alt == self.altlim[ 0 ] else append( self.Uwind, Uwind, axis=1 )
            self.Vwind = Vwind if _alt == self.altlim[ 0 ] else append( self.Vwind, Vwind, axis=1 )

        self.glatbins = hwm14Obj.glatbins

        self.Uwind = transpose(self.Uwind)
        self.Vwind = transpose(self.Vwind)

    #
    # End of 'LatVsHeiArray'
    #####

    def LonVsHeiArray(self):

        """     """

        self.altbins = arange(self.altlim[0], self.altlim[1] + self.altstp, self.altstp)

        for alt in self.altbins:

            if True:

                hwm14Obj = HWM14(alt=alt, ap=self.ap, glat=self.glat,
                    glonlim=self.glonlim, glonstp=self.glonstp, 
                    option=self.option, verbose=self.verbose, ut=self.ut )

            else:

                pass

            Uwind = reshape( hwm14Obj.Uwind, ( len( hwm14Obj.Uwind ), 1 ) )
            Vwind = reshape( hwm14Obj.Vwind, ( len( hwm14Obj.Vwind ), 1 ) )
            self.Uwind = Uwind if alt == self.altlim[ 0 ] else append( self.Uwind, Uwind, axis=1 )
            self.Vwind = Vwind if alt == self.altlim[ 0 ] else append( self.Vwind, Vwind, axis=1 )

        self.glonbins = hwm14Obj.glonbins

        self.Uwind = transpose(self.Uwind)
        self.Vwind = transpose(self.Vwind)
                            
    #
    # End of 'LonVsHeiArray'
    #####

    def LonVsLatArray(self):

        """  """
        
        self.glatbins = arange(self.glatlim[0], self.glatlim[1] + self.glatstp, self.glatstp)

        for glat in self.glatbins:

            hwm14Obj = HWM14(alt=self.alt, ap=self.ap, glat=glat,
                glonlim=self.glonlim, glonstp=self.glonstp, 
                option=4, verbose=self.verbose, ut=self.ut )

            Uwind = reshape( hwm14Obj.Uwind, ( len( hwm14Obj.Uwind ), 1 ) )
            Vwind = reshape( hwm14Obj.Vwind, ( len( hwm14Obj.Vwind ), 1 ) )
            self.Uwind = Uwind if glat == self.glatlim[ 0 ] else append( self.Uwind, Uwind, axis=1 )
            self.Vwind = Vwind if glat == self.glatlim[ 0 ] else append( self.Vwind, Vwind, axis=1 )

        self.glonbins = hwm14Obj.glonbins

        self.Uwind = transpose(self.Uwind)
        self.Vwind = transpose(self.Vwind)
                            
    #
    # End of 'LonVsHeiArray'
    #####
            

    def LatVsGMTArray(self):
        pass
    #
    # End of 'LatVsGMTArray'
    #####

#
# End of 'HWM142D'
#####


class HWM142DPlot:

    def __init__( self, profObj=None ):

        """
            Constructor of class resposible of graphical reports for the
            Horizontal Wind Model 14. It requires the methods (instance)
            returned by class "HWM142D"
        """

        if profObj != None:

            self.option = profObj.option

            self.year, self.doy = profObj.year, profObj.doy
            self.ut = profObj.ut
            if self.option != 1: self.alt = profObj.alt
            if self.option != 2 and self.option != 6: self.glat = profObj.glat
            if self.option != 4 and self.option != 6: self.glon = profObj.glon
            self.ap = profObj.ap
            
            if self.option >= 1 and self.option <= 6:
                self.Uwind = profObj.Uwind
                self.Vwind = profObj.Vwind
            valid = True
            if self.option == 1:
                self.altbins = profObj.altbins
                self.altlim = profObj.altlim
                self.utbins = profObj.utbins
                self.utlim = profObj.utlim
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
            elif self.option == 4:
                self.glonbins = profObj.glonbins
                self.glonlim = profObj.glonlim
                self.altbins = profObj.altbins
                self.altlim = profObj.altlim
                self.LonVsHeiPlot()                
            elif self.option == 6:
                self.glonbins = profObj.glonbins
                self.glonlim = profObj.glonlim
                self.glatbins = profObj.glatbins
                self.glatlim = profObj.glatlim
                self.LonVsLatPlot()
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

    def GetHHMMSS(self):
        hh = floor(self.ut)
        dummy = self.ut - hh
        mm = floor(dummy * 60)
        dummy = dummy * 60 - mm
        self.second = int(floor(dummy * 60))
        self.hour, self.minute = int(hh), int(mm)
    #
    # End of 'GetHHMMSS'
    #####

    def GetTitle(self):

        dateStr = 'DATE: {:4d}.{:03d}'.format(self.year, self.doy)

        self.GetHHMMSS()
        timeStr = 'TIME: {:02d}:{:02d} UT'.format(self.hour, self.minute)

        apStr = 'ap: {:3d}'.format(self.ap[1])
        
        try:
            altStr = 'ALT: {:7.2f}'.format(self.alt)
        except:
            pass

        try:
            latStr = '{:6.2f}$^\circ${:s}'.format(abs(self.glat),
                'N' if self.glat > 0 else 'S')
        except:
            pass

        try:
            lonStr = '{:6.2f}$^\circ${:s}'.format(abs(self.glon),
                'E' if self.glon > 0 else 'W')
        except:
            pass

        try:
            locStr = '{:s}, {:s}'.format(latStr, lonStr)
        except:
            pass

        if self.option == 1:
            self.title = '{:s} - {:s} - {:s}'.format(dateStr, apStr, locStr)
        elif self.option == 2:
            self.title = '{:s} - {:s} - {:s} - GEOG. LON.: {:s}'.format(dateStr, timeStr, apStr, lonStr)
        elif self.option == 4:
            self.title = '{:s} - {:s} - {:s} - GEOG. LAT.: {:s}'.format(dateStr, timeStr, apStr, latStr)
        elif self.option == 6:
            self.title = '{:s} - {:s} - {:s} - {:s}'.format(dateStr, timeStr, apStr, altStr)

    #
    # End of 'GetTitle'
    #####

    def XVsY2DPlot( self, ax, xVal, yVal, zVal, cmap=None, title=None,
        xlabel=None, xlim=None, ylabel=None, ylim=None, zlabel=None, zMax=None, zMin=None ):

        X, Y = pylab.meshgrid( xVal, yVal )
        X = transpose( X )
        Y = transpose( Y )

        C = transpose( zVal )
        ipn = ax.pcolor( X, Y, C, cmap=cmap, edgecolors='None', norm=pylab.Normalize(), 
            vmax=zMax, vmin=zMin )
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

        self.GetTitle()

        cmap = pylab.cm.RdBu_r

        fig = pylab.figure( figsize=(15,6) )

        ax = pylab.subplot(121)

        self.XVsY2DPlot( ax, self.utbins, self.altbins, self.Uwind, cmap=cmap,
            title=self.title, xlabel=r'Hour (GMT)', xlim=self.utlim, ylabel=r'Altitude (km)',
            ylim=self.altlim, zlabel=r'Zonal (U), m/s', zMax=None, zMin=None )

        ax = pylab.subplot(122)

        self.XVsY2DPlot( ax, self.utbins, self.altbins, self.Vwind, cmap=cmap,
            title=self.title, xlabel=r'Hour (GMT)', xlim=self.utlim, ylabel=r'Altitude (km)',
            ylim=self.altlim, zlabel=r'Meridional (V), m/s', zMax=None, zMin=None )

    #
    # End of 'HeiProfPlot'
    #####

    def LatVsHeiPlot(self):

        self.GetTitle()

        cmap = pylab.cm.RdBu_r

        fig = pylab.figure( figsize=(15,6) )

        ax = pylab.subplot(121)

        self.XVsY2DPlot( ax, self.glatbins, self.altbins, self.Uwind, cmap=cmap, 
            title=self.title, xlabel=r'Geog. Lat. ($^o$)', xlim=self.glatlim, 
            ylabel=r'Altitude (km)', ylim=self.altlim, zlabel=r'Zonal (U), m/s', 
            zMax=None, zMin=None )

        ax = pylab.subplot(122)

        self.XVsY2DPlot( ax, self.glatbins, self.altbins, self.Vwind, cmap=cmap, 
            title=self.title, xlabel=r'Geog. Lat. ($^o$)', 
            xlim=self.glatlim, ylabel=r'Altitude (km)', ylim=self.altlim, 
            zlabel=r'Meridional (V), m/s', zMax=None, zMin=None )

    #
    # End of 'LatVsHeiPlot'
    #####

    def LonVsHeiPlot(self):

        self.GetTitle()

        cmap = pylab.cm.RdBu_r

        fig = pylab.figure( figsize=(15,6) )

        ax = pylab.subplot(121)

        self.XVsY2DPlot( ax, self.glonbins, self.altbins, self.Uwind, cmap=cmap, 
            title=self.title, xlabel=r'Geog. Lon. ($^o$)', xlim=self.glonlim, 
            ylabel=r'Altitude (km)', ylim=self.altlim, zlabel=r'Zonal (U), m/s', 
            zMax=None, zMin=None )

        ax = pylab.subplot(122)

        self.XVsY2DPlot( ax, self.glonbins, self.altbins, self.Vwind, cmap=cmap, 
            title=self.title, xlabel=r'Geog. Lon. ($^o$)', 
            xlim=self.glonlim, ylabel=r'Altitude (km)', ylim=self.altlim, 
            zlabel=r'Meridional (V), m/s', zMax=None, zMin=None )

    #
    # End of 'LonVsHeiPlot'
    #####

    def LonVsLatPlot(self):

        self.GetTitle()

        cmap = pylab.cm.RdBu_r

        fig = pylab.figure( figsize=(15,6) )

        ax = pylab.subplot(121)

        self.XVsY2DPlot( ax, self.glonbins, self.glatbins, self.Uwind, cmap=cmap, 
            title=self.title, xlabel=r'Geog. Lon. ($^o$)', xlim=self.glonlim, 
            ylabel=r'Geog. Lat. ($^o$)', ylim=self.glatlim, zlabel=r'Zonal (U), m/s', 
            zMax=None, zMin=None )

        ax = pylab.subplot(122)

        self.XVsY2DPlot( ax, self.glonbins, self.glatbins, self.Vwind, cmap=cmap, 
            title=self.title, xlabel=r'Geog. Lon. ($^o$)', 
            xlim=self.glonlim, ylabel=r'Geog. Lat. ($^o$)', ylim=self.glatlim, 
            zlabel=r'Meridional (V), m/s', zMax=None, zMin=None )

    #
    # End of 'LonVsLatPlot'
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