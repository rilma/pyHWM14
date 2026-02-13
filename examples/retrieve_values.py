#!/usr/bin/env python
"""
Example script demonstrating how to retrieve zonal and meridional wind values
from the HWM14 model for specific parameters.

This script shows various ways to use pyHWM14 to get wind values at specific
date/time, location, and altitude.
"""

from datetime import datetime
from pyhwm2014 import HWM14


def example_single_point():
    """
    Retrieve wind values at a single point in space and time.
    
    This is the most common use case - getting wind values for a specific
    location, date/time, and altitude.
    """
    print("=" * 70)
    print("Example 1: Single Point Retrieval")
    print("=" * 70)
    
    # Define parameters
    year = 2023
    day_of_year = 150  # Day 150 is approximately May 30
    universal_time = 12.0  # 12:00 UT (noon)
    altitude_km = 300.0  # 300 km altitude
    latitude = 40.0  # 40°N
    longitude = -105.0  # 105°W
    ap_index = 10  # Geomagnetic activity index
    
    print(f"\nParameters:")
    print(f"  Date: Year {year}, Day of Year {day_of_year}")
    print(f"  Time: {universal_time} UT")
    print(f"  Location: {latitude}°N, {longitude}°E")
    print(f"  Altitude: {altitude_km} km")
    print(f"  ap index: {ap_index}")
    
    # Create HWM14 object with a single altitude
    # Note: We use option=1 (height profile) but with a single altitude point
    hwm14 = HWM14(
        alt=altitude_km,
        altlim=[altitude_km, altitude_km],
        altstp=1,
        year=year,
        day=day_of_year,
        ut=universal_time,
        glat=latitude,
        glon=longitude,
        ap=[-1, ap_index],
        option=1,
        verbose=False
    )
    
    # Extract wind values
    # Uwind = Zonal wind (positive eastward)
    # Vwind = Meridional wind (positive northward)
    zonal_wind = hwm14.Uwind[0]
    meridional_wind = hwm14.Vwind[0]
    
    print(f"\nResults:")
    print(f"  Zonal wind (U): {zonal_wind:.2f} m/s")
    print(f"  Meridional wind (V): {meridional_wind:.2f} m/s")
    print(f"  Total horizontal wind: {(zonal_wind**2 + meridional_wind**2)**0.5:.2f} m/s")
    

def example_height_profile():
    """
    Retrieve wind values at multiple altitudes for a single location and time.
    
    This creates a vertical profile of winds.
    """
    print("\n" + "=" * 70)
    print("Example 2: Height Profile")
    print("=" * 70)
    
    # Define parameters
    year = 2023
    day_of_year = 180
    universal_time = 14.5  # 14:30 UT
    altitude_min = 100.0
    altitude_max = 400.0
    altitude_step = 50.0
    latitude = -30.0  # 30°S
    longitude = 150.0  # 150°E
    ap_index = 5
    
    print(f"\nParameters:")
    print(f"  Date: Year {year}, Day of Year {day_of_year}")
    print(f"  Time: {universal_time} UT")
    print(f"  Location: {latitude}°N, {longitude}°E")
    print(f"  Altitude range: {altitude_min}-{altitude_max} km")
    print(f"  Altitude step: {altitude_step} km")
    print(f"  ap index: {ap_index}")
    
    # Create HWM14 object for height profile
    hwm14 = HWM14(
        altlim=[altitude_min, altitude_max],
        altstp=altitude_step,
        year=year,
        day=day_of_year,
        ut=universal_time,
        glat=latitude,
        glon=longitude,
        ap=[-1, ap_index],
        option=1,  # Height profile option
        verbose=False
    )
    
    print(f"\nResults:")
    print(f"{'Altitude (km)':>15} {'Zonal U (m/s)':>15} {'Meridional V (m/s)':>20}")
    print("-" * 52)
    for i, alt in enumerate(hwm14.altbins):
        print(f"{alt:>15.1f} {hwm14.Uwind[i]:>15.2f} {hwm14.Vwind[i]:>20.2f}")


def example_with_datetime():
    """
    Example showing how to convert a datetime object to year and day-of-year.
    """
    print("\n" + "=" * 70)
    print("Example 3: Using Python datetime")
    print("=" * 70)
    
    # Use a datetime object
    dt = datetime(2024, 7, 15, 18, 30)  # July 15, 2024, 18:30
    
    # Convert to year and day of year
    year = dt.year
    day_of_year = dt.timetuple().tm_yday
    # Convert time to decimal hours UT
    universal_time = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    
    # Location and other parameters
    altitude_km = 250.0
    latitude = 0.0  # Equator
    longitude = 0.0  # Prime Meridian
    ap_index = 15
    
    print(f"\nInput datetime: {dt}")
    print(f"Converted to:")
    print(f"  Year: {year}")
    print(f"  Day of Year: {day_of_year}")
    print(f"  Universal Time: {universal_time:.4f} hours")
    print(f"  Location: {latitude}°N, {longitude}°E")
    print(f"  Altitude: {altitude_km} km")
    
    # Get wind values
    hwm14 = HWM14(
        alt=altitude_km,
        altlim=[altitude_km, altitude_km],
        altstp=1,
        year=year,
        day=day_of_year,
        ut=universal_time,
        glat=latitude,
        glon=longitude,
        ap=[-1, ap_index],
        option=1,
        verbose=False
    )
    
    print(f"\nResults:")
    print(f"  Zonal wind (U): {hwm14.Uwind[0]:.2f} m/s")
    print(f"  Meridional wind (V): {hwm14.Vwind[0]:.2f} m/s")


def example_multiple_locations():
    """
    Retrieve wind values at multiple latitudes (latitude profile).
    """
    print("\n" + "=" * 70)
    print("Example 4: Latitude Profile")
    print("=" * 70)
    
    # Parameters
    year = 2023
    day_of_year = 1
    universal_time = 0.0
    altitude_km = 200.0
    latitude_min = -90.0
    latitude_max = 90.0
    latitude_step = 30.0
    longitude = 0.0
    ap_index = 10
    
    print(f"\nParameters:")
    print(f"  Date: Year {year}, Day of Year {day_of_year}")
    print(f"  Time: {universal_time} UT")
    print(f"  Longitude: {longitude}°E")
    print(f"  Altitude: {altitude_km} km")
    print(f"  Latitude range: {latitude_min}° to {latitude_max}°")
    print(f"  Latitude step: {latitude_step}°")
    
    # Get latitude profile
    hwm14 = HWM14(
        alt=altitude_km,
        glatlim=[latitude_min, latitude_max],
        glatstp=latitude_step,
        glon=longitude,
        year=year,
        day=day_of_year,
        ut=universal_time,
        ap=[-1, ap_index],
        option=2,  # Latitude profile option
        verbose=False
    )
    
    print(f"\nResults:")
    print(f"{'Latitude (°)':>15} {'Zonal U (m/s)':>15} {'Meridional V (m/s)':>20}")
    print("-" * 52)
    for i, lat in enumerate(hwm14.glatbins):
        print(f"{lat:>15.1f} {hwm14.Uwind[i]:>15.2f} {hwm14.Vwind[i]:>20.2f}")


def main():
    """
    Run all examples.
    """
    print("\n" + "=" * 70)
    print("pyHWM14: Horizontal Wind Model 2014")
    print("Examples of retrieving zonal and meridional wind values")
    print("=" * 70)
    
    # Run examples
    example_single_point()
    example_height_profile()
    example_with_datetime()
    example_multiple_locations()
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("\nNotes:")
    print("- Zonal wind (U): Positive = Eastward, Negative = Westward")
    print("- Meridional wind (V): Positive = Northward, Negative = Southward")
    print("- ap index: Geomagnetic activity index (higher = more disturbed)")
    print("- Altitude is in kilometers")
    print("- All wind values are in meters per second (m/s)")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
