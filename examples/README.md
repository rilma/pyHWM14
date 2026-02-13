# Examples

This directory contains example scripts demonstrating how to use pyHWM14 to retrieve wind values.

## Available Examples

### retrieve_values.py

A comprehensive example script showing various ways to retrieve zonal and meridional wind values:

1. **Single Point Retrieval**: Get wind values at a specific location, date/time, and altitude
2. **Height Profile**: Get wind values at multiple altitudes
3. **Using Python datetime**: Convert datetime objects to HWM14 parameters
4. **Latitude Profile**: Get wind values at multiple latitudes

**Usage:**
```bash
python examples/retrieve_values.py
```

## Understanding the Output

- **Zonal wind (U)**: East-west component
  - Positive values = Eastward wind
  - Negative values = Westward wind

- **Meridional wind (V)**: North-south component
  - Positive values = Northward wind
  - Negative values = Southward wind

All wind values are in meters per second (m/s).

## Common Use Cases

### Get wind at a single point

```python
from pyhwm2014 import HWM14

hwm14 = HWM14(
    alt=300.0,           # Altitude in km
    altlim=[300.0, 300.0],  # Same as alt for single point
    altstp=1,            # Step size (not used for single point)
    year=2023,           # Year
    day=150,             # Day of year (1-366)
    ut=12.0,             # Universal time in hours (0-24)
    glat=40.0,           # Latitude in degrees (-90 to 90)
    glon=-105.0,         # Longitude in degrees (-180 to 180)
    ap=[-1, 10],         # ap[1] is the geomagnetic index
    option=1,            # Option 1 = height profile
    verbose=False        # Set to True to see detailed output
)

zonal_wind = hwm14.Uwind[0]       # m/s
meridional_wind = hwm14.Vwind[0]  # m/s
```

### Get vertical wind profile

```python
from pyhwm2014 import HWM14

hwm14 = HWM14(
    altlim=[100.0, 400.0],  # Altitude range
    altstp=50.0,            # Step size
    year=2023,
    day=150,
    ut=12.0,
    glat=40.0,
    glon=-105.0,
    ap=[-1, 10],
    option=1,
    verbose=False
)

# Results are arrays
for i, alt in enumerate(hwm14.altbins):
    print(f"Alt: {alt} km, U: {hwm14.Uwind[i]:.2f} m/s, V: {hwm14.Vwind[i]:.2f} m/s")
```

## Parameters Reference

| Parameter | Description | Range/Format |
|-----------|-------------|--------------|
| `year` | Year | YYYY (e.g., 2023) |
| `day` | Day of year | 1-366 |
| `ut` | Universal time | 0-24 (decimal hours) |
| `glat` | Geographic latitude | -90 to 90 degrees |
| `glon` | Geographic longitude | -180 to 180 degrees |
| `alt` | Altitude | kilometers |
| `altlim` | Altitude range | [min, max] in km |
| `altstp` | Altitude step | kilometers |
| `ap` | Geomagnetic index | [-1, value] where value is 0-400 |
| `option` | Profile type | 1=height, 2=latitude, 3=time, 4=longitude |
| `verbose` | Print details | True/False |

## See Also

- `../scripts/retrieve.py` - Command-line interface for retrieving values
- Main README.rst - Full documentation
