"""Plotting utilities for HWM14 model results."""

from typing import TYPE_CHECKING

import numpy as np
from numpy import append, arange, ceil, floor, meshgrid

if TYPE_CHECKING:
    from matplotlib.figure import Figure
    from matplotlib.axes import Axes
    from mpl_toolkits.basemap import Basemap

# Optional matplotlib imports
try:
    from matplotlib.colors import Normalize
    from matplotlib.pyplot import cm, figure, show, subplots
except (ImportError, RuntimeError):
    cm = None  # type: ignore
    figure = None  # type: ignore
    show = None  # type: ignore
    subplots = None  # type: ignore
    Normalize = None  # type: ignore

# Optional Basemap import
try:
    from mpl_toolkits.basemap import Basemap
except ImportError:
    Basemap = None  # type: ignore


class HWM14Plot:
    """Graphical representation of HWM14 1D profile results.
    
    Parameters
    ----------
    profObj : HWM14, optional
        HWM14 instance with calculated profile data.
    
    Attributes
    ----------
    Uwind : list[float]
        Zonal wind component.
    Vwind : list[float]
        Meridional wind component.
    """

    def __init__(self, profObj: "HWM14 | None" = None) -> None:
        """Initialize plotting for HWM14 profile."""
        if profObj is not None:
            self.option = profObj.option

            self.year = profObj.year
            self.doy = profObj.doy
            if self.option != 3:
                self.ut = profObj.ut
            if self.option != 2:
                self.glat = profObj.glat
            if self.option != 4:
                self.glon = profObj.glon
            if self.option != 1:
                self.alt = profObj.alt
            self.ap = profObj.ap

            if 1 <= self.option <= 4:
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
                print("Invalid option!")
                valid = False

            if valid and figure is not None:
                show()
        else:
            print("Wrong inputs!")

    def GetHHMMSS(self) -> None:
        """Convert decimal hours to hours, minutes, seconds."""
        hh = floor(self.ut)
        dummy = self.ut - hh
        mm = floor(dummy * 60)
        dummy = dummy * 60 - mm
        self.second = int(floor(dummy * 60))
        self.hour = int(hh)
        self.minute = int(mm)

    def GetTitle(self) -> None:
        """Generate plot title with metadata."""
        dateStr = f"DATE: {self.year:4d}.{self.doy:03d}"

        try:
            self.GetHHMMSS()
            timeStr = f"TIME: {self.hour:02d}:{self.minute:02d} UT"
        except Exception:
            timeStr = ""

        apStr = f"ap: {self.ap[1]:3d}"

        try:
            altStr = f"ALT: {self.alt:7.2f} km"
        except Exception:
            altStr = ""

        try:
            latStr = r"{:6.2f}$^\circ${:s}".format(
                abs(self.glat), "N" if self.glat > 0 else "S"
            )
        except Exception:
            latStr = ""

        try:
            lonStr = r"{:6.2f}$^\circ${:s}".format(
                abs(self.glon), "E" if self.glon > 0 else "W"
            )
        except Exception:
            lonStr = ""

        try:
            locStr = f"{latStr:s}, {lonStr:s}"
        except Exception:
            locStr = ""

        if self.option == 1:
            self.title = f"{dateStr:s} - {timeStr:s} - {apStr:s} - {locStr:s}"
        elif self.option == 2:
            self.title = (
                f"{dateStr:s} - {timeStr:s} - {apStr:s} - {altStr:s} - "
                f"GEOG. LON.: {lonStr:s}"
            )
        elif self.option == 3:
            self.title = f"{dateStr:s} - {apStr:s} - {altStr:s} - {locStr:s}"
        elif self.option == 4:
            self.title = (
                f"{dateStr:s} - {timeStr:s} - {apStr:s} - {altStr:s} - "
                f"GEOG. LAT.: {latStr:s}"
            )

    def HeiProfPlot(self) -> None:
        """Plot height profile with zonal and meridional winds."""
        if figure is None:
            return

        self.GetTitle()

        ax = figure().gca()
        ax.plot(self.Uwind, self.altbins, label="U")
        ax.plot(self.Vwind, self.altbins, label="V")
        ax.set_ylim(self.altbins[[0, -1]])
        ax.set_title(self.title)
        ax.set_xlabel(r"(m/s)")
        ax.set_ylabel(r"(km)")
        ax.legend(loc="best")

    def LatProfPlot(self) -> None:
        """Plot latitude profile with zonal and meridional winds."""
        if figure is None:
            return

        self.GetTitle()

        ax = figure().gca()
        ax.plot(self.glatbins, self.Uwind, label="U")
        ax.plot(self.glatbins, self.Vwind, label="V")
        ax.set_xlim(self.glatbins[[0, -1]])
        ax.set_title(self.title)
        ax.set_xlabel(r"Geog. Lat. ($^\circ$)")
        ax.set_ylabel(r"Wind speed (m/s)")
        ax.legend(loc="best")

    def GMTProfPlot(self) -> None:
        """Plot GMT profile with zonal and meridional winds."""
        if figure is None:
            return

        self.GetTitle()

        ax = figure().gca()
        ax.plot(self.utbins, self.Uwind, label="U")
        ax.plot(self.utbins, self.Vwind, label="V")
        ax.set_xlim(self.utbins[[0, -1]])
        ax.set_title(self.title)
        ax.set_xlabel(r"Hour (GMT)")
        ax.set_ylabel(r"Wind speed (m/s)")
        ax.legend(loc="best")

    def LonProfPlot(self) -> None:
        """Plot longitude profile with zonal and meridional winds."""
        if figure is None:
            return

        self.GetTitle()

        ax = figure().gca()
        ax.plot(self.glonbins, self.Uwind, label="U")
        ax.plot(self.glonbins, self.Vwind, label="V")
        ax.set_xlim(self.glonbins[[0, -1]])
        ax.set_title(self.title)
        ax.set_xlabel(r"Geog. Lon. ($^\circ$)")
        ax.set_ylabel(r"Wind speed (m/s)")
        ax.legend(loc="best")


class HWM142DPlot:
    """Graphical representation of HWM142D 2D array results.
    
    Parameters
    ----------
    profObj : HWM142D, optional
        HWM142D instance with calculated 2D array data.
    WF : bool, optional
        If True, use wind field (vector) plot; if False, use scalar plots.
        Default is False.
    zMax : list[float], optional
        Maximum values for color scale [U_max, V_max]. Default is [None, None].
    zMin : list[float], optional
        Minimum values for color scale [U_min, V_min]. Default is [None, None].
    """

    def __init__(
        self,
        profObj: "HWM142D | None" = None,
        WF: bool = False,
        zMax: list[float | None] | None = None,
        zMin: list[float | None] | None = None,
    ) -> None:
        """Initialize plotting for HWM142D 2D profiles."""
        if zMax is None:
            zMax = [None, None]
        if zMin is None:
            zMin = [None, None]

        if profObj is not None:
            self.zMin = zMin
            self.zMax = zMax
            self.WF = WF

            self.option = profObj.option

            self.year = profObj.year
            self.doy = profObj.doy
            self.ut = profObj.ut
            if self.option != 1:
                self.alt = profObj.alt
            if self.option != 2 and self.option != 6:
                self.glat = profObj.glat
            if self.option != 4 and self.option != 6:
                self.glon = profObj.glon
            self.ap = profObj.ap

            if 1 <= self.option <= 6:
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
                print("Invalid option!")
                valid = False

            if valid and figure is not None:
                show()
        else:
            print("Wrong inputs!")

    def GetHHMMSS(self) -> None:
        """Convert decimal hours to hours, minutes, seconds."""
        hh = floor(self.ut)
        dummy = self.ut - hh
        mm = floor(dummy * 60)
        dummy = dummy * 60 - mm
        self.second = int(floor(dummy * 60))
        self.hour = int(hh)
        self.minute = int(mm)

    def GetTitle(self) -> None:
        """Generate plot title with metadata."""
        dateStr = f"DATE: {self.year:4d}.{self.doy:03d}"

        self.GetHHMMSS()
        timeStr = f"TIME: {self.hour:02d}:{self.minute:02d} UT"

        apStr = f"ap: {self.ap[1]:3d}"

        try:
            altStr = f"ALT: {self.alt:7.2f} km"
        except Exception:
            altStr = ""

        try:
            latStr = r"{:6.2f}$^\circ${:s}".format(
                abs(self.glat), "N" if self.glat > 0 else "S"
            )
        except Exception:
            latStr = ""

        try:
            lonStr = r"{:6.2f}$^\circ${:s}".format(
                abs(self.glon), "E" if self.glon > 0 else "W"
            )
        except Exception:
            lonStr = ""

        try:
            locStr = f"{latStr:s}, {lonStr:s}"
        except Exception:
            locStr = ""

        if self.option == 1:
            self.title = f"{dateStr:s} - {apStr:s} - {locStr:s}"
        elif self.option == 2:
            self.title = (
                f"{dateStr:s} - {timeStr:s} - {apStr:s} - "
                f"GEOG. LON.: {lonStr:s}"
            )
        elif self.option == 4:
            self.title = (
                f"{dateStr:s} - {timeStr:s} - {apStr:s} - "
                f"GEOG. LAT.: {latStr:s}"
            )
        elif self.option == 6:
            self.title = f"{dateStr:s} - {timeStr:s} - {apStr:s} - {altStr:s}"

    def XVsY2DWindMap(
        self,
        ax: "Axes",
        xVal: np.ndarray,
        yVal: np.ndarray,
        uVal: np.ndarray,
        vVal: np.ndarray,
        title: str | None = None,
        xlabel: str | None = None,
        xlim: list[float] | None = None,
        ylabel: str | None = None,
        ylim: list[float] | None = None,
        zlabel: str | None = None,
        zMax: float | None = None,
        zMin: float | None = None,
    ) -> None:
        """Create 2D wind vector map using Basemap."""
        if Basemap is None:
            return

        m = Basemap(
            llcrnrlon=self.glonlim[0],
            llcrnrlat=self.glatlim[0],
            urcrnrlon=self.glonlim[-1],
            urcrnrlat=self.glatlim[-1],
            resolution="l",
        )

        m.drawcoastlines()

        # Lines at constant "latitude"
        parallelsLim = self._RoundLim([yVal[0], yVal[-1]])
        m.drawparallels(
            arange(parallelsLim[0], parallelsLim[1], 20.0),
            labels=[True, False, False, True],
        )

        # Lines at constant "longitude"
        meridiansLim = self._RoundLim([xVal[0], xVal[-1]])
        m.drawmeridians(
            arange(meridiansLim[0], meridiansLim[1], 30.0),
            labels=[True, False, False, True],
        )

        X, Y = meshgrid(xVal, yVal)
        totalWind = (uVal**2 + vVal**2) ** 0.5

        ipc = m.quiver(
            X,
            Y,
            uVal.T,
            vVal.T,
            totalWind.T,
            alpha=0.5,
            angles="uv",
            cmap=cm.jet,
            pivot="middle",
            units="xy",
        )
        m.quiver(
            X,
            Y,
            uVal.T,
            vVal.T,
            angles="uv",
            edgecolor="k",
            facecolor="None",
            linewidth=0.5,
            pivot="middle",
            units="xy",
        )

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_title(title)

        cbpn = m.colorbar(ipc)
        cbpn.set_label(zlabel)

    def XVsY2DMap(
        self,
        ax: "Axes",
        xVal: np.ndarray,
        yVal: np.ndarray,
        zVal: np.ndarray,
        cmap: str | None = None,
        title: str | None = None,
        xlabel: str | None = None,
        xlim: list[float] | None = None,
        ylabel: str | None = None,
        ylim: list[float] | None = None,
        zlabel: str | None = None,
        zMax: float | None = None,
        zMin: float | None = None,
    ) -> None:
        """Create 2D scalar map using Basemap."""
        if Basemap is None:
            return

        m = Basemap(
            llcrnrlon=self.glonlim[0],
            llcrnrlat=self.glatlim[0],
            urcrnrlon=self.glonlim[-1],
            urcrnrlat=self.glatlim[-1],
            resolution="l",
        )

        m.drawcoastlines()

        # Lines at constant "latitude"
        parallelsLim = self._RoundLim([yVal[0], yVal[-1]])
        m.drawparallels(
            arange(parallelsLim[0], parallelsLim[1], 20.0),
            labels=[True, False, False, True],
        )

        # Lines at constant "longitude"
        meridiansLim = self._RoundLim([xVal[0], xVal[-1]])
        m.drawmeridians(
            arange(meridiansLim[0], meridiansLim[1], 30.0),
            labels=[True, False, False, True],
        )

        X, Y = meshgrid(xVal, yVal)
        m.pcolor(
            X,
            Y,
            zVal.T,
            cmap=cmap,
            edgecolors="None",
            norm=Normalize(),
            vmax=zMax,
            vmin=zMin,
        )

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_title(title)

        cbpn = m.colorbar(ipc)
        cbpn.set_label(zlabel)

    def XVsY2DPlot(
        self,
        ax: "Axes",
        xVal: np.ndarray,
        yVal: np.ndarray,
        zVal: np.ndarray,
        cmap: str | None = None,
        title: str | None = None,
        xlabel: str | None = None,
        xlim: list[float] | None = None,
        ylabel: str | None = None,
        ylim: list[float] | None = None,
        zlabel: str | None = None,
        zMax: float | None = None,
        zMin: float | None = None,
    ) -> None:
        """Create 2D scalar plot."""
        if figure is None:
            return

        X, Y = meshgrid(xVal, yVal)
        X = X.T
        Y = Y.T

        C = zVal.T
        ipn = ax.pcolor(
            X,
            Y,
            C,
            cmap=cmap,
            edgecolors="None",
            norm=Normalize(),
            vmax=zMax,
            vmin=zMin,
        )
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        cbpn = ax.figure.colorbar(ipn, ax=ax)
        cbpn.set_label(zlabel)

    def HeiVsLTPlot(self) -> None:
        """Plot height vs local time with U and V components."""
        if figure is None:
            return

        self.GetTitle()

        cmap = cm.RdBu_r

        fg, axs = subplots(1, 2, figsize=(15, 6))

        self.XVsY2DPlot(
            axs[0],
            self.utbins,
            self.altbins,
            self.Uwind,
            cmap=cmap,
            title=self.title,
            xlabel=r"Hour (GMT)",
            xlim=self.utlim,
            ylabel=r"Altitude (km)",
            ylim=self.altlim,
            zlabel=r"Zonal (U), m/s",
            zMax=self.zMax[0],
            zMin=self.zMin[0],
        )

        self.XVsY2DPlot(
            axs[1],
            self.utbins,
            self.altbins,
            self.Vwind,
            cmap=cmap,
            title=self.title,
            xlabel=r"Hour (GMT)",
            xlim=self.utlim,
            ylabel=r"Altitude (km)",
            ylim=self.altlim,
            zlabel=r"Meridional (V), m/s",
            zMax=self.zMax[1],
            zMin=self.zMin[1],
        )

    def LatVsHeiPlot(self) -> None:
        """Plot latitude vs height with U and V components."""
        if figure is None:
            return

        self.GetTitle()

        cmap = cm.RdBu_r

        fg, axs = subplots(1, 2, figsize=(15, 6))

        self.XVsY2DPlot(
            axs[0],
            self.glatbins,
            self.altbins,
            self.Uwind,
            cmap=cmap,
            title=self.title,
            xlabel=r"Geog. Lat. ($^o$)",
            xlim=self.glatlim,
            ylabel=r"Altitude (km)",
            ylim=self.altlim,
            zlabel=r"Zonal (U), m/s",
            zMax=self.zMax[0],
            zMin=self.zMin[0],
        )

        self.XVsY2DPlot(
            axs[1],
            self.glatbins,
            self.altbins,
            self.Vwind,
            cmap=cmap,
            title=self.title,
            xlabel=r"Geog. Lat. ($^o$)",
            xlim=self.glatlim,
            ylabel=r"Altitude (km)",
            ylim=self.altlim,
            zlabel=r"Meridional (V), m/s",
            zMax=self.zMax[1],
            zMin=self.zMin[1],
        )

    def LonVsHeiPlot(self) -> None:
        """Plot longitude vs height with U and V components."""
        if figure is None:
            return

        self.GetTitle()

        cmap = cm.RdBu_r

        fg, axs = subplots(1, 2, figsize=(15, 6))

        self.XVsY2DPlot(
            axs[0],
            self.glonbins,
            self.altbins,
            self.Uwind,
            cmap=cmap,
            title=self.title,
            xlabel=r"Geog. Lon. ($^o$)",
            xlim=self.glonlim,
            ylabel=r"Altitude (km)",
            ylim=self.altlim,
            zlabel=r"Zonal (U), m/s",
            zMax=self.zMax[0],
            zMin=self.zMin[0],
        )

        self.XVsY2DPlot(
            axs[1],
            self.glonbins,
            self.altbins,
            self.Vwind,
            cmap=cmap,
            title=self.title,
            xlabel=r"Geog. Lon. ($^o$)",
            xlim=self.glonlim,
            ylabel=r"Altitude (km)",
            ylim=self.altlim,
            zlabel=r"Meridional (V), m/s",
            zMax=self.zMax[1],
            zMin=self.zMin[1],
        )

    def LonVsLatPlot(self) -> None:
        """Plot longitude vs latitude with U and V components."""
        if figure is None:
            return

        self.GetTitle()

        if not self.WF:
            cmap = cm.RdBu_r

            fg, axs = subplots(2, 1, figsize=(8, 8))
            self.XVsY2DMap(
                axs[0],
                self.glonbins,
                self.glatbins,
                self.Uwind,
                cmap=cmap,
                title=self.title,
                xlabel=r"Geog. Lon. ($^o$)",
                xlim=self.glonlim,
                ylabel=r"Geog. Lat. ($^o$)",
                ylim=self.glatlim,
                zlabel=r"Zonal (U), m/s",
                zMax=self.zMax[0],
                zMin=self.zMin[0],
            )

            self.XVsY2DMap(
                axs[1],
                self.glonbins,
                self.glatbins,
                self.Vwind,
                cmap=cmap,
                title=self.title,
                xlabel=r"Geog. Lon. ($^o$)",
                xlim=self.glonlim,
                ylabel=r"Geog. Lat. ($^o$)",
                ylim=self.glatlim,
                zlabel=r"Meridional (V), m/s",
                zMax=self.zMax[1],
                zMin=self.zMin[1],
            )
        else:
            ax = figure(figsize=(16, 12)).gca()
            self.XVsY2DWindMap(
                ax,
                self.glonbins,
                self.glatbins,
                self.Uwind,
                self.Vwind,
                title=self.title,
                xlabel=r"Geog. Lon. ($^o$)",
                xlim=self.glonlim,
                ylabel=r"Geog. Lat. ($^o$)",
                ylim=self.glatlim,
                zlabel="Wind (m/s)",
                zMax=self.zMax[0],
                zMin=self.zMin[0],
            )

    def _RoundLim(self, lim: list[float]) -> list[float]:
        """Round limit values to nearest 10.
        
        Parameters
        ----------
        lim : list[float]
            [min, max] limit values.
            
        Returns
        -------
        list[float]
            Rounded limit values.
        """
        return [floor(lim[0] / 10.0) * 10.0, ceil(lim[1] / 10.0) * 10.0]
