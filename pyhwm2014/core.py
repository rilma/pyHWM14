"""HWM14 core model classes for wind speed calculations."""

import logging
from typing import Literal

import numpy as np
from numpy import append, arange, ones, reshape

from . import hwm14


class HWM14:
    """Horizontal Wind Model version 2014 (HWM14) interface.
    
    Calculates zonal and meridional wind components at various atmospheric
    profiles (height, latitude, GMT, longitude).
    
    Parameters
    ----------
    alt : float, optional
        Altitude in kilometers. Default is 300.0.
    altlim : list[float], optional
        Altitude range [min, max] in km. Default is [0., 400.].
    altstp : float, optional
        Altitude resolution in km. Default is 25.
    ap : list[int], optional
        AP index: [not_used, 3hr_ap_index]. Default is [-1, 35].
    f107 : float, optional
        F10.7 solar flux index. Default is -1.
    f107a : float, optional
        F10.7 average solar flux index. Default is -1.
    day : int, optional
        Day of year (1-366). Default is 323.
    glat : float, optional
        Geographic latitude in degrees. Default is -11.95.
    glatlim : list[float], optional
        Latitude range [min, max] in degrees. Default is [-10., 10.].
    glatstp : float, optional
        Latitude resolution in degrees. Default is 2.
    glon : float, optional
        Geographic longitude in degrees. Default is -76.77.
    glonlim : list[float], optional
        Longitude range [min, max] in degrees. Default is [-20., 20.].
    glonstp : float, optional
        Longitude resolution in degrees. Default is 2.
    option : Literal[1, 2, 3, 4], optional
        Profile selection:
        - 1: Height profile (varies altitude)
        - 2: Latitude profile (varies latitude)
        - 3: GMT profile (varies UTC time)
        - 4: Longitude profile (varies longitude)
        Default is 1.
    stl : float, optional
        Solar local time in hours (not used). Default is -1.
    ut : float, optional
        Universal time (UTC) in hours. Default is 12.
    utlim : list[float], optional
        UTC range [min, max] in hours. Default is [0., 23.].
    utstp : float, optional
        UTC resolution in hours. Default is 1.
    verbose : bool, optional
        Print message to screen during calculation. Default is True.
    year : int, optional
        Year (YYYY). Default is 1993.
    
    Attributes
    ----------
    Uwind : list[float]
        Zonal wind component (m/s) for each profile point.
    Vwind : list[float]
        Meridional wind component (m/s) for each profile point.
    altbins : ndarray
        Altitude values (km) for option=1.
    glatbins : ndarray
        Latitude values (degrees) for option=2.
    utbins : ndarray
        UTC values (hours) for option=3.
    glonbins : ndarray
        Longitude values (degrees) for option=4.
    
    Examples
    --------
    >>> hwm = HWM14(altlim=[90, 200], altstp=1, ap=[-1, 35],
    ...             day=323, option=1, ut=11.66667, verbose=False, year=1993)
    >>> len(hwm.Uwind)
    111
    """

    def __init__(
        self,
        alt: float = 300.0,
        altlim: list[float] | None = None,
        altstp: float = 25.0,
        ap: list[int] | None = None,
        f107: float = -1.0,
        f107a: float = -1.0,
        day: int = 323,
        glat: float = -11.95,
        glatlim: list[float] | None = None,
        glatstp: float = 2.0,
        glon: float = -76.77,
        glonlim: list[float] | None = None,
        glonstp: float = 2.0,
        option: Literal[1, 2, 3, 4] = 1,
        stl: float = -1.0,
        ut: float = 12.0,
        utlim: list[float] | None = None,
        utstp: float = 1.0,
        verbose: bool = True,
        year: int = 1993,
    ) -> None:
        """Initialize HWM14 model calculation."""
        # Apply defaults to mutable arguments
        if altlim is None:
            altlim = [0.0, 400.0]
        if ap is None:
            ap = [-1, 35]
        if glatlim is None:
            glatlim = [-10.0, 10.0]
        if glonlim is None:
            glonlim = [-20.0, 20.0]
        if utlim is None:
            utlim = [0.0, 23.0]

        self.option = option
        self.year = year
        self.doy = day

        # Initialize wind arrays early (before validation)
        self.Uwind: list[float] = []
        self.Vwind: list[float] = []

        # Validate option and set profile-specific parameters
        if option == 1:  # Height profile
            self.glat = glat
            self.glon = glon
            self.stl = stl
            self.altlim = altlim
            self.altstp = altstp
        elif option == 2:  # Latitude profile
            self.alt = alt
            self.glon = glon
            self.stl = stl
            self.glatlim = glatlim
            self.glatstp = glatstp
        elif option == 3:  # GMT profile
            self.alt = alt
            self.glat = glat
            self.glon = glon
            self.utlim = utlim
            self.utstp = utstp
        elif option == 4:  # Longitude profile
            self.ut = ut
            self.alt = alt
            self.glat = glat
            self.glonlim = glonlim
            self.glonstp = glonstp
            self.stl = stl
        else:
            logging.error("Invalid option! Must be 1, 2, 3, or 4.")
            return

        self.iyd = int((year - (2000 if year > 1999 else 1900)) * 1000) + day

        if option != 3:
            self.sec = ut * 3600.0
            self.stl = stl
            self.ut = ut

        self.ap = ap
        self.apqt = -ones(2)  # Required for quiet time component

        self.f107 = f107
        self.f107a = f107a
        self.verbose = verbose

        # Execute appropriate profile calculation
        if "alt" not in self.__dict__:
            self.HeiProfile()
        elif "glat" not in self.__dict__:
            self.LatProfile()
        elif "ut" not in self.__dict__:
            self.GMTProfile()
        elif "glon" not in self.__dict__:
            self.LonProfile()
        else:
            print()

    def HeiProfile(self) -> None:
        """Calculate height profile (varying altitude)."""
        if self.verbose:
            print("HEIGHT PROFILE")
            print("                 quiet         disturbed             total")
            print(" alt      mer      zon      mer      zon      mer      zon")

        self.altbins = arange(
            self.altlim[0], self.altlim[1] + self.altstp, self.altstp
        )

        for alt in self.altbins:
            wqt = hwm14.hwm14(
                self.iyd,
                self.sec,
                alt,
                self.glat,
                self.glon,
                self.stl,
                self.f107a,
                self.f107,
                self.apqt,
            )

            wdt = hwm14.dwm07(self.iyd, self.sec, alt, self.glat, self.glon, self.ap)

            w = hwm14.hwm14(
                self.iyd,
                self.sec,
                alt,
                self.glat,
                self.glon,
                self.stl,
                self.f107a,
                self.f107,
                self.ap,
            )

            if self.verbose:
                print(
                    " %3i %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f"
                    % (alt, wqt[0], wqt[1], wdt[0], wdt[1], w[0], w[1])
                )

            self.Uwind.append(w[1])
            self.Vwind.append(w[0])

    def LatProfile(self) -> None:
        """Calculate latitude profile (varying latitude)."""
        if self.verbose:
            print("LATITUDE PROFILE")
            print("                   quiet         disturbed             total")
            print("  glat      mer      zon      mer      zon      mer      zon")

        self.glatbins = arange(
            self.glatlim[0], self.glatlim[1] + self.glatstp, self.glatstp
        )

        for glat in self.glatbins:
            wqt = hwm14.hwm14(
                self.iyd,
                self.sec,
                self.alt,
                glat,
                self.glon,
                self.stl,
                self.f107a,
                self.f107,
                self.apqt,
            )

            wdt = hwm14.dwm07(self.iyd, self.sec, self.alt, glat, self.glon, self.ap)

            w = hwm14.hwm14(
                self.iyd,
                self.sec,
                self.alt,
                glat,
                self.glon,
                self.stl,
                self.f107a,
                self.f107,
                self.ap,
            )

            if self.verbose:
                print(
                    " %5.1f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f"
                    % (glat, wqt[0], wqt[1], wdt[0], wdt[1], w[0], w[1])
                )

            self.Uwind.append(w[1])
            self.Vwind.append(w[0])

    def GMTProfile(self) -> None:
        """Calculate GMT profile (varying UTC time)."""
        if self.verbose:
            print("GMT PROFILE")
            print("                   quiet         disturbed             total")
            print("   stl      mer      zon      mer      zon      mer      zon")

        self.utbins = arange(
            self.utlim[0], self.utlim[1] + self.utstp, self.utstp
        )
        self.mltbins: list[float] = []

        for ut in self.utbins:
            self.toMLT(ut)
            self.mltbins.append(self.mlt)

            sec = ut * 3600.0

            wqt = hwm14.hwm14(
                self.iyd,
                sec,
                self.alt,
                self.glat,
                self.glon,
                -1,
                self.f107a,
                self.f107,
                self.apqt,
            )

            wdt = hwm14.dwm07(self.iyd, sec, self.alt, self.glat, self.glon, self.ap)

            w = hwm14.hwm14(
                self.iyd,
                sec,
                self.alt,
                self.glat,
                self.glon,
                -1,
                self.f107a,
                self.f107,
                self.ap,
            )

            if self.verbose:
                print(
                    " %5.1f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f"
                    % (ut, wqt[0], wqt[1], wdt[0], wdt[1], w[0], w[1])
                )

            self.Uwind.append(w[1])
            self.Vwind.append(w[0])

    def LonProfile(self) -> None:
        """Calculate longitude profile (varying longitude)."""
        if self.verbose:
            print("LONGITUDE PROFILE")
            print("                   quiet         disturbed             total")
            print("  glon      mer      zon      mer      zon      mer      zon")

        self.glonbins = arange(
            self.glonlim[0], self.glonlim[1] + self.glonstp, self.glonstp
        )

        for glon in self.glonbins:
            wqt = hwm14.hwm14(
                self.iyd,
                self.sec,
                self.alt,
                self.glat,
                glon,
                -1,
                self.f107a,
                self.f107,
                self.apqt,
            )

            wdt = hwm14.dwm07(self.iyd, self.sec, self.alt, self.glat, glon, self.ap)

            w = hwm14.hwm14(
                self.iyd,
                self.sec,
                self.alt,
                self.glat,
                glon,
                -1,
                self.f107a,
                self.f107,
                self.ap,
            )

            if self.verbose:
                print(
                    " %5.1f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f"
                    % (glon, wqt[0], wqt[1], wdt[0], wdt[1], w[0], w[1])
                )

            self.Uwind.append(w[1])
            self.Vwind.append(w[0])

    def toMLT(self, ut: float) -> None:
        """Calculate magnetic local time.
        
        Parameters
        ----------
        ut : float
            Universal time (UTC) in hours.
        """
        hwm14.inithwm()
        mlat, mlon, f1e, f1n, f2e, f2n = hwm14.gd2qd(self.glat, self.glon)
        self.mlt = hwm14.mltcalc(mlat, mlon, self.doy, ut)


class HWM142D:
    """2D array calculations for HWM14 with varying two parameters.
    
    Parameters
    ----------
    option : Literal[1, 2, 3, 4, 5, 6], optional
        Profile selection:
        - 1: Time vs Height (varies UTC and altitude)
        - 2: Latitude vs Height (varies latitude and altitude)
        - 3: GMT vs Latitude (varies UTC and latitude)
        - 4: Longitude vs Height (varies longitude and altitude)
        - 5: GMT vs Longitude (varies UTC and longitude)
        - 6: Longitude vs Latitude (varies longitude and latitude)
        Default is 1.
    **kwargs
        Additional keyword arguments passed to individual profile calculations.
        See HWM14 for parameter descriptions.
    
    Attributes
    ----------
    Uwind : ndarray
        2D array of zonal wind components (m/s).
    Vwind : ndarray
        2D array of meridional wind components (m/s).
    """

    def __init__(
        self,
        alt: float = 300.0,
        altlim: list[float] | None = None,
        altstp: float = 25.0,
        ap: list[int] | None = None,
        day: int = 323,
        f107: float = -1.0,
        f107a: float = -1.0,
        glat: float = -11.95,
        glatlim: list[float] | None = None,
        glatstp: float = 5.0,
        glon: float = -76.77,
        glonlim: list[float] | None = None,
        glonstp: float = 5.0,
        option: Literal[1, 2, 3, 4, 5, 6] = 1,
        stl: float = -1.0,
        utlim: list[float] | None = None,
        utstp: float = 1.0,
        ut: float = 12.0,
        verbose: bool = True,
        year: int = 1993,
    ) -> None:
        """Initialize 2D HWM14 calculation."""
        # Apply defaults to mutable arguments
        if altlim is None:
            altlim = [0.0, 400.0]
        if ap is None:
            ap = [-1, 35]
        if glatlim is None:
            glatlim = [-40.0, 40.0]
        if glonlim is None:
            glonlim = [-40.0, 40.0]
        if utlim is None:
            utlim = [0.0, 24.0]

        self.option = option
        self.year = year
        self.doy = day
        if option not in [3, 5]:
            self.ut = ut

        if option == 1:  # Time vs Height
            self.glat = glat
            self.glon = glon
            self.stl = stl
            self.utlim = utlim
            self.utstp = utstp
            self.altlim = altlim
            self.altstp = altstp
        elif option == 2:  # Latitude vs Height
            self.alt = alt
            self.glon = glon
            self.stl = stl
            self.altlim = altlim
            self.altstp = altstp
            self.glatlim = glatlim
            self.glatstp = glatstp
        elif option == 3:  # GMT vs Latitude
            self.alt = alt
            self.glon = glon
            self.glatlim = glatlim
            self.glatstp = glatstp
            self.utlim = utlim
            self.utstp = utstp
        elif option == 4:  # Longitude vs Height
            self.alt = alt
            self.glat = glat
            self.altlim = altlim
            self.altstp = altstp
            self.glonlim = glonlim
            self.glonstp = glonstp
        elif option == 5:  # GMT vs Longitude
            self.alt = alt
            self.glon = glon
            self.glonlim = glonlim
            self.glonstp = glonstp
            self.utlim = utlim
            self.utstp = utstp
        elif option == 6:  # Longitude vs Latitude
            self.alt = alt
            self.glatlim = glatlim
            self.glatstp = glatstp
            self.glonlim = glonlim
            self.glonstp = glonstp
        else:
            logging.error("Invalid option! Must be 1-6.")
            return

        self.iyd = int((year - (2000 if year > 1999 else 1900)) * 10000) + day
        if option != 3:
            self.sec = ut * 3600.0
        self.ap = ap
        self.apqt = -ones(2)

        self.f107 = f107
        self.f107a = f107a
        self.verbose = verbose

        self.Uwind: list[np.ndarray] = []
        self.Vwind: list[np.ndarray] = []

        # Execute appropriate 2D profile calculation
        if "alt" not in self.__dict__:
            self.HeiVsLTArray()
        elif (
            "glat" not in self.__dict__
            and "glon" not in self.__dict__
        ):
            self.LonVsLatArray()
        elif (
            "glat" not in self.__dict__
            and "ut" not in self.__dict__
        ):
            self.LatVsGMTArray()
        elif "glat" not in self.__dict__:
            self.LatVsHeiArray()
        elif "glon" not in self.__dict__:
            self.LonVsHeiArray()
        else:
            print("")

    def HeiVsLTArray(self) -> None:
        """Calculate height vs local time 2D array."""
        self.utbins = arange(self.utlim[0], self.utlim[1] + self.utstp, self.utstp)

        for ut in self.utbins:
            hwm14obj = HWM14(
                altlim=self.altlim,
                altstp=self.altstp,
                ap=self.ap,
                glat=self.glat,
                glon=self.glon,
                option=1,
                ut=ut,
                verbose=self.verbose,
            )

            uwind = reshape(hwm14obj.Uwind, (len(hwm14obj.Uwind), 1))
            vwind = reshape(hwm14obj.Vwind, (len(hwm14obj.Vwind), 1))
            self.Uwind = (
                uwind
                if ut == self.utlim[0]
                else append(self.Uwind, uwind, axis=1)
            )
            self.Vwind = (
                vwind
                if ut == self.utlim[0]
                else append(self.Vwind, vwind, axis=1)
            )

        self.altbins = hwm14obj.altbins

    def LatVsHeiArray(self) -> None:
        """Calculate latitude vs height 2D array."""
        self.altbins = arange(
            self.altlim[0], self.altlim[1] + self.altstp, self.altstp
        )

        for _alt in self.altbins:
            hwm14obj = HWM14(
                alt=_alt,
                ap=self.ap,
                glatlim=self.glatlim,
                glatstp=self.glatstp,
                glon=self.glon,
                option=2,
                verbose=self.verbose,
                ut=self.ut,
            )

            uwind = reshape(hwm14obj.Uwind, (len(hwm14obj.Uwind), 1))
            vwind = reshape(hwm14obj.Vwind, (len(hwm14obj.Vwind), 1))
            self.Uwind = (
                uwind
                if _alt == self.altlim[0]
                else append(self.Uwind, uwind, axis=1)
            )
            self.Vwind = (
                vwind
                if _alt == self.altlim[0]
                else append(self.Vwind, vwind, axis=1)
            )

        self.glatbins = hwm14obj.glatbins

        self.Uwind = self.Uwind.T
        self.Vwind = self.Vwind.T

    def LonVsHeiArray(self) -> None:
        """Calculate longitude vs height 2D array."""
        self.altbins = arange(
            self.altlim[0], self.altlim[1] + self.altstp, self.altstp
        )

        for alt in self.altbins:
            hwm14obj = HWM14(
                alt=alt,
                ap=self.ap,
                glat=self.glat,
                glonlim=self.glonlim,
                glonstp=self.glonstp,
                option=4,
                verbose=self.verbose,
                ut=self.ut,
            )

            uwind = reshape(hwm14obj.Uwind, (len(hwm14obj.Uwind), 1))
            vwind = reshape(hwm14obj.Vwind, (len(hwm14obj.Vwind), 1))
            self.Uwind = (
                uwind
                if alt == self.altlim[0]
                else append(self.Uwind, uwind, axis=1)
            )
            self.Vwind = (
                vwind
                if alt == self.altlim[0]
                else append(self.Vwind, vwind, axis=1)
            )

        self.glonbins = hwm14obj.glonbins

        self.Uwind = self.Uwind.T
        self.Vwind = self.Vwind.T

    def LonVsLatArray(self) -> None:
        """Calculate longitude vs latitude 2D array."""
        self.glatbins = arange(
            self.glatlim[0], self.glatlim[1] + self.glatstp, self.glatstp
        )

        for glat in self.glatbins:
            hwm14obj = HWM14(
                alt=self.alt,
                ap=self.ap,
                glat=glat,
                glonlim=self.glonlim,
                glonstp=self.glonstp,
                option=4,
                verbose=self.verbose,
                ut=self.ut,
            )

            uwind = reshape(hwm14obj.Uwind, (len(hwm14obj.Uwind), 1))
            vwind = reshape(hwm14obj.Vwind, (len(hwm14obj.Vwind), 1))
            self.Uwind = (
                uwind
                if glat == self.glatlim[0]
                else append(self.Uwind, uwind, axis=1)
            )
            self.Vwind = (
                vwind
                if glat == self.glatlim[0]
                else append(self.Vwind, vwind, axis=1)
            )

        self.glonbins = hwm14obj.glonbins

        self.Uwind = self.Uwind.T
        self.Vwind = self.Vwind.T

    def LatVsGMTArray(self) -> None:
        """Calculate latitude vs GMT 2D array."""
        pass
