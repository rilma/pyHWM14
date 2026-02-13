#!/usr/bin/env python
"""
CLI tool for retrieving wind values from the HWM14 model.

This script provides a simple command-line interface to retrieve zonal and
meridional wind values for specific parameters.

Usage:
    python retrieve.py --year 2023 --day 150 --time 12.0 --lat 40.0 --lon -105.0 --alt 300.0
    python retrieve.py --year 2023 --day 150 --time 12.0 --lat 40.0 --lon -105.0 --alt-range 100 400 50
"""

import argparse
import sys
from datetime import datetime
from pyhwm2014 import HWM14


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Retrieve wind values from HWM14 model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single point retrieval
  %(prog)s --year 2023 --day 150 --time 12.0 --lat 40.0 --lon -105.0 --alt 300.0
  
  # Height profile
  %(prog)s --year 2023 --day 150 --time 12.0 --lat 40.0 --lon -105.0 --alt-range 100 400 50
  
  # Using datetime format
  %(prog)s --datetime "2023-05-30 12:00:00" --lat 40.0 --lon -105.0 --alt 300.0
  
  # Latitude profile
  %(prog)s --year 2023 --day 150 --time 12.0 --lon -105.0 --alt 300.0 --lat-range -90 90 30
        """
    )
    
    # Date/time options
    date_group = parser.add_mutually_exclusive_group(required=True)
    date_group.add_argument('--datetime', type=str,
                           help='Date and time in format "YYYY-MM-DD HH:MM:SS"')
    date_group.add_argument('--year', type=int,
                           help='Year (YYYY)')
    
    parser.add_argument('--day', type=int,
                       help='Day of year (1-366)')
    parser.add_argument('--time', type=float,
                       help='Universal time in decimal hours (0-24)')
    
    # Location options
    parser.add_argument('--lat', '--latitude', type=float, dest='latitude',
                       help='Geographic latitude in degrees (-90 to 90)')
    parser.add_argument('--lon', '--longitude', type=float, dest='longitude',
                       help='Geographic longitude in degrees (-180 to 180)')
    
    # Altitude options
    alt_group = parser.add_mutually_exclusive_group(required=True)
    alt_group.add_argument('--alt', '--altitude', type=float, dest='altitude',
                          help='Altitude in kilometers')
    alt_group.add_argument('--alt-range', nargs=3, type=float, metavar=('MIN', 'MAX', 'STEP'),
                          help='Altitude range: min max step (in km)')
    
    # Latitude profile option
    parser.add_argument('--lat-range', nargs=3, type=float, metavar=('MIN', 'MAX', 'STEP'),
                       help='Latitude range for profile: min max step (in degrees)')
    
    # Longitude profile option
    parser.add_argument('--lon-range', nargs=3, type=float, metavar=('MIN', 'MAX', 'STEP'),
                       help='Longitude range for profile: min max step (in degrees)')
    
    # Other parameters
    parser.add_argument('--ap', type=int, default=10,
                       help='Geomagnetic ap index (default: 10)')
    parser.add_argument('--verbose', action='store_true',
                       help='Show verbose output')
    parser.add_argument('--json', action='store_true',
                       help='Output results in JSON format')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.year and not args.day:
        parser.error('--day is required when using --year')
    if args.year and not args.time:
        parser.error('--time is required when using --year')
    
    return args


def parse_datetime_string(dt_string):
    """Parse datetime string and return year, day_of_year, and universal_time."""
    try:
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
        except ValueError:
            dt = datetime.strptime(dt_string, "%Y-%m-%d")
    
    year = dt.year
    day_of_year = dt.timetuple().tm_yday
    universal_time = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    
    return year, day_of_year, universal_time


def retrieve_single_point(year, day, time, lat, lon, alt, ap, verbose=False):
    """Retrieve wind values at a single point."""
    hwm14 = HWM14(
        alt=alt,
        altlim=[alt, alt],
        altstp=1,
        year=year,
        day=day,
        ut=time,
        glat=lat,
        glon=lon,
        ap=[-1, ap],
        option=1,
        verbose=verbose
    )
    
    return {
        'zonal': hwm14.Uwind[0],
        'meridional': hwm14.Vwind[0],
        'altitude': alt,
        'latitude': lat,
        'longitude': lon
    }


def retrieve_height_profile(year, day, time, lat, lon, alt_range, ap, verbose=False):
    """Retrieve wind values at multiple altitudes."""
    alt_min, alt_max, alt_step = alt_range
    
    hwm14 = HWM14(
        altlim=[alt_min, alt_max],
        altstp=alt_step,
        year=year,
        day=day,
        ut=time,
        glat=lat,
        glon=lon,
        ap=[-1, ap],
        option=1,
        verbose=verbose
    )
    
    results = []
    for i, alt in enumerate(hwm14.altbins):
        results.append({
            'altitude': float(alt),
            'zonal': float(hwm14.Uwind[i]),
            'meridional': float(hwm14.Vwind[i])
        })
    
    return results


def retrieve_latitude_profile(year, day, time, lon, alt, lat_range, ap, verbose=False):
    """Retrieve wind values at multiple latitudes."""
    lat_min, lat_max, lat_step = lat_range
    
    hwm14 = HWM14(
        alt=alt,
        glatlim=[lat_min, lat_max],
        glatstp=lat_step,
        glon=lon,
        year=year,
        day=day,
        ut=time,
        ap=[-1, ap],
        option=2,
        verbose=verbose
    )
    
    results = []
    for i, lat in enumerate(hwm14.glatbins):
        results.append({
            'latitude': float(lat),
            'zonal': float(hwm14.Uwind[i]),
            'meridional': float(hwm14.Vwind[i])
        })
    
    return results


def retrieve_longitude_profile(year, day, time, lat, alt, lon_range, ap, verbose=False):
    """Retrieve wind values at multiple longitudes."""
    lon_min, lon_max, lon_step = lon_range
    
    hwm14 = HWM14(
        alt=alt,
        glat=lat,
        glonlim=[lon_min, lon_max],
        glonstp=lon_step,
        year=year,
        day=day,
        ut=time,
        ap=[-1, ap],
        option=4,
        verbose=verbose
    )
    
    results = []
    for i, lon in enumerate(hwm14.glonbins):
        results.append({
            'longitude': float(lon),
            'zonal': float(hwm14.Uwind[i]),
            'meridional': float(hwm14.Vwind[i])
        })
    
    return results


def print_results(results, args):
    """Print results in human-readable or JSON format."""
    if args.json:
        import json
        print(json.dumps(results, indent=2))
        return
    
    # Human-readable output
    print("\n" + "=" * 70)
    print("HWM14 Wind Retrieval Results")
    print("=" * 70)
    
    if isinstance(results, dict):
        # Single point
        print(f"\nLocation: {results['latitude']:.2f}°N, {results['longitude']:.2f}°E")
        print(f"Altitude: {results['altitude']:.2f} km")
        print(f"\nZonal wind (U):      {results['zonal']:>10.2f} m/s")
        print(f"Meridional wind (V): {results['meridional']:>10.2f} m/s")
        total_wind = (results['zonal']**2 + results['meridional']**2)**0.5
        print(f"Total wind speed:    {total_wind:>10.2f} m/s")
    else:
        # Profile
        if 'altitude' in results[0]:
            print(f"\n{'Altitude (km)':>15} {'Zonal U (m/s)':>15} {'Meridional V (m/s)':>20}")
            print("-" * 52)
            for r in results:
                print(f"{r['altitude']:>15.1f} {r['zonal']:>15.2f} {r['meridional']:>20.2f}")
        elif 'latitude' in results[0]:
            print(f"\n{'Latitude (°)':>15} {'Zonal U (m/s)':>15} {'Meridional V (m/s)':>20}")
            print("-" * 52)
            for r in results:
                print(f"{r['latitude']:>15.1f} {r['zonal']:>15.2f} {r['meridional']:>20.2f}")
        elif 'longitude' in results[0]:
            print(f"\n{'Longitude (°)':>15} {'Zonal U (m/s)':>15} {'Meridional V (m/s)':>20}")
            print("-" * 52)
            for r in results:
                print(f"{r['longitude']:>15.1f} {r['zonal']:>15.2f} {r['meridional']:>20.2f}")
    
    print("\n" + "=" * 70 + "\n")


def main():
    """Main function."""
    args = parse_arguments()
    
    # Parse date/time
    if args.datetime:
        year, day, time = parse_datetime_string(args.datetime)
    else:
        year = args.year
        day = args.day
        time = args.time
    
    try:
        # Determine which retrieval mode to use
        if args.lat_range:
            # Latitude profile
            if not args.longitude:
                print("Error: --lon is required for latitude profile", file=sys.stderr)
                sys.exit(1)
            if args.altitude:
                results = retrieve_latitude_profile(
                    year, day, time, args.longitude, args.altitude,
                    args.lat_range, args.ap, args.verbose
                )
            else:
                print("Error: --alt is required for latitude profile", file=sys.stderr)
                sys.exit(1)
        elif args.lon_range:
            # Longitude profile
            if not args.latitude:
                print("Error: --lat is required for longitude profile", file=sys.stderr)
                sys.exit(1)
            if args.altitude:
                results = retrieve_longitude_profile(
                    year, day, time, args.latitude, args.altitude,
                    args.lon_range, args.ap, args.verbose
                )
            else:
                print("Error: --alt is required for longitude profile", file=sys.stderr)
                sys.exit(1)
        elif args.alt_range:
            # Height profile
            if not args.latitude or not args.longitude:
                print("Error: --lat and --lon are required for height profile", file=sys.stderr)
                sys.exit(1)
            results = retrieve_height_profile(
                year, day, time, args.latitude, args.longitude,
                args.alt_range, args.ap, args.verbose
            )
        else:
            # Single point
            if not args.latitude or not args.longitude:
                print("Error: --lat and --lon are required for single point retrieval", file=sys.stderr)
                sys.exit(1)
            results = retrieve_single_point(
                year, day, time, args.latitude, args.longitude,
                args.altitude, args.ap, args.verbose
            )
        
        print_results(results, args)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
