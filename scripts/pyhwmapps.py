
from matplotlib.pyplot import colorbar, figure, show
from numpy.ma import masked_where
from pyhwm2014.pyhwm14 import HWM142D
from pyhwm2014 import hwm14
import pyapex
from pylab import cm, Normalize
from scipy import arange, asarray, isnan, nan, tile, transpose, where
from timeutil.timeutil import TimeUtilities


class HWM14_2DProf(HWM142D):

    def __init__(self):

        HWM142D.__init__(self, verbose=False)        


    def LatVsFL(self, date=[2003,11,21], time=[23,15,0], gc=[-77.76,-11.95],
            hlim=[80.,200.], hstp=1., mlatlim=[-10.,10.], mlatstp=.1):

        #
        # INPUTS
        #

        # Date
        year, month, day = date

        # Time
        hour, minute, second = time

        # Geog. Coord.
        dlon, dlat = gc

        # hlim -> Height range at equator, in km
        # hstp -> height resolution at equator, in km
        # mlatlim -> Geom. latitude range, in degrees
        # mlatstp -> Geom. latitude resolution, in degrees

        #
        ###

        self.hlim = hlim

        doy = TimeUtilities().CalcDOY(year, month, day)
        date = year + doy / (365 + 1 if TimeUtilities().IsLeapYear else 0)

        self.coordl = []

        for h in arange(hlim[0], hlim[1] + hstp, hstp):

            gc, qc = pyapex.ApexFL().getFL(date=date, dlon=dlon, dlat=dlat, hateq=h, mlatRange=mlatlim, mlatSTP=mlatstp)

            self.coordl.append([gc['lon'], gc['alt'], gc['lat']])

        self.coordl = asarray(self.coordl)

        # nfl -> No. of field-line (or height)
        # nc -> No. of coord. (0 -> lon, 1 -> alt, 2 -> lat)
        # np -> No. of points per field-line
        nfl, nc, np = self.coordl.shape

        self.Uwind, self.Vwind = tile(nan, (np, nfl)),  tile(nan, (np, nfl))      
        
        iyd = int((year - (2000 if year >= 2000 else 1900)) * 1e3) + doy
        sec = (hour + minute / 60 + second / 3600) * 3600
        stl, f107a, f107, ap = 17., 90, 90, [2,2]

        for fl in range(nfl):

            curr_coordl = transpose(self.coordl[fl, :, :])

            ind = where(curr_coordl[:, 1] >= hlim[0])

            if len(ind[0]) > 0:

                ns, dummy = curr_coordl[ind[0], :].shape

                for s in range(ns):

                    glon, alt, glat = curr_coordl[ind[0][s], :] 

                    w = hwm14.hwm14( iyd, sec, alt, glat, glon, stl, f107a, f107, ap )

                    self.Uwind[ind[0][s], fl] = w[1]
                    self.Vwind[ind[0][s], fl] = w[0]


    #
    # End of 'LatVsFL' 
    #####


    def PlotLatVsFL(self):

        xlabel, ylabel = r'Geog. Lat. ($^o$)', r'(km)'

        nrow, ncol = 1, 2

        spID = nrow * 100 + ncol * 10

        counter = 0

        X, Y = transpose(self.coordl[:,  2, :]), transpose(self.coordl[:, 1, :])

        f = figure(figsize=(16,6))

        for ir in range(nrow):

            for ic in range(ncol):

                pn = f.add_subplot(spID + (counter + 1))

                if counter == 0:
                    Z = self.Uwind
                    vmin, vmax = -50, 50
                    title=r'Zonal wind (U)'
                    
                elif counter == 1:
                    Z = self.Vwind
                    vmin, vmax = -100, 100
                    title=r'Meridional wind (V)'

                Z_masked = masked_where(isnan(Z), Z)
                ipc = pn.pcolor(X, Y, Z_masked, cmap=cm.RdBu_r, edgecolors='None', 
                    norm=Normalize(), vmax=vmax, vmin=vmin)

                # pn.set_xlim( xlim )
                # pn.set_ylim( ylim )
                pn.set_title( title )
                pn.set_xlabel( xlabel )
                pn.set_ylabel( ylabel )
                    
                cp = colorbar(ipc)
                pn.set_ylim(self.hlim)
                pn.invert_xaxis()

                counter += 1

    #
    # End of 'PlotLatVsFL' 
    #####



if __name__ == '__main__':

    Obj = HWM14_2DProf()
    Obj.LatVsFL(hlim=[80.,200.], hstp=2., mlatlim=[-10.,10.], mlatstp=.5)
    #Obj.LatVsFL(hlim=[100.,1000.], hstp=10., mlatlim=[-20.,20.], mlatstp=1.)
    Obj.PlotLatVsFL()
    show()
