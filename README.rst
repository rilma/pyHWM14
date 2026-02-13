.. image:: https://github.com/rilma/pyHWM14/actions/workflows/ci.yaml/badge.svg
    :target: https://github.com/rilma/pyHWM14/actions/workflows/ci.yaml
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.240890.svg
   :target: http://doi.org/10.5281/zenodo.240890
   
=======
pyHWM14
=======
Python interface for the Horizontal Wind Model version 2014 (HWM14)

.. contents::


Installation
============

----------------
From Source Code
----------------

Currently supports Python 3.10 under Ubuntu 20.04 (see Github Actions).

IMPORTANT: For support in other Python versions and/or OS, users are invited to work on the case and submmit a PR. Help making the project more generic!

.. code-block:: bash

    $ git clone https://github.com/rilma/pyHWM14.git
    $ cd pyHWM14
    $ make install

-------------------
Make Targets (3.10)
-------------------

The repository includes additional ``make`` targets to set up and use a local Python 3.10 environment.

.. list-table::
     :header-rows: 1

     * - Target
         - Purpose
     * - ``make install-python310``
         - Installs Python 3.10 with ``uv`` (if needed) and pins ``.python-version`` to 3.10.
     * - ``make venv310``
         - Creates/recreates a local ``.venv`` using Python 3.10.
     * - ``make install310``
         - Installs project dependencies and runs ``setup.py develop`` inside ``.venv``.
     * - ``make test310``
         - Runs the test suite with coverage using ``.venv`` Python 3.10.

Typical workflow:

.. code-block:: bash

        $ make install310
        $ source .venv/bin/activate
        $ make test310

---------
From PyPi
---------

::

    pip install pyhwm2014

Testing
=======

.. code-block:: bash

    $ make test

Getting Started
===============

This section provides a quick guide to retrieving zonal and meridional wind values from the HWM14 model.

-----------------
Basic Concepts
-----------------

The HWM14 model provides **zonal** (east-west) and **meridional** (north-south) wind components in the upper atmosphere. To retrieve wind values, you need to specify:

* **Date/Time**: Year, day of year (1-366), and universal time (0-24 hours)
* **Location**: Geographic latitude (-90° to 90°) and longitude (-180° to 180°)
* **Altitude**: Height above Earth's surface in kilometers
* **Geomagnetic Activity**: The ap index (default: -1 for climatology)

**Wind Components:**

* **Zonal wind (U)**: Positive = Eastward, Negative = Westward
* **Meridional wind (V)**: Positive = Northward, Negative = Southward

All wind values are in meters per second (m/s).

--------------------------
Quick Start: Single Point
--------------------------

Retrieve wind values at a specific location, date/time, and altitude:

.. code-block:: python

    from pyhwm2014 import HWM14
    
    # Define parameters
    year = 2023
    day_of_year = 150  # Approximately May 30
    universal_time = 12.0  # 12:00 UT (noon)
    altitude_km = 300.0  # 300 km altitude
    latitude = 40.0  # 40°N
    longitude = -105.0  # 105°W
    ap_index = 10  # Geomagnetic activity index
    
    # Retrieve wind values
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
    
    # Access results
    zonal_wind = hwm14.Uwind[0]  # m/s
    meridional_wind = hwm14.Vwind[0]  # m/s
    
    print(f"Zonal wind: {zonal_wind:.2f} m/s")
    print(f"Meridional wind: {meridional_wind:.2f} m/s")

--------------------------------
Using Python datetime Objects
--------------------------------

Convert Python datetime to required parameters:

.. code-block:: python

    from datetime import datetime
    from pyhwm2014 import HWM14
    
    # Your datetime
    dt = datetime(2024, 7, 15, 18, 30)  # July 15, 2024, 18:30
    
    # Convert to HWM14 parameters
    year = dt.year
    day_of_year = dt.timetuple().tm_yday
    universal_time = dt.hour + dt.minute / 60.0
    
    # Now use with HWM14
    hwm14 = HWM14(
        alt=250.0,
        altlim=[250.0, 250.0],
        altstp=1,
        year=year,
        day=day_of_year,
        ut=universal_time,
        glat=0.0,
        glon=0.0,
        ap=[-1, 10],
        option=1,
        verbose=False
    )

-----------------------
Command-Line Interface
-----------------------

Use the CLI tool for quick retrievals without writing code:

.. code-block:: bash

    # Single point retrieval
    $ python scripts/retrieve.py --year 2023 --day 150 --time 12.0 \
        --lat 40.0 --lon -105.0 --alt 300.0

    # Height profile (multiple altitudes)
    $ python scripts/retrieve.py --year 2023 --day 150 --time 12.0 \
        --lat 40.0 --lon -105.0 --alt-range 100 400 50

    # Using datetime format
    $ python scripts/retrieve.py --datetime "2023-05-30 12:00:00" \
        --lat 40.0 --lon -105.0 --alt 300.0

    # Get JSON output
    $ python scripts/retrieve.py --year 2023 --day 150 --time 12.0 \
        --lat 40.0 --lon -105.0 --alt 300.0 --json

----------------
More Examples
----------------

For comprehensive examples including height profiles, latitude profiles, and more, see:

* ``examples/retrieve_values.py`` - Detailed Python examples
* ``scripts/`` directory - Various example scripts

Run the comprehensive example:

.. code-block:: bash

    $ python examples/retrieve_values.py

Examples
========

You will need seaborn (the statistical data visualization package) in order to run the following examples.

.. code-block:: bash

    $ pip install seaborn


--------------
Height Profile
--------------


.. code-block:: bash

    >>> from pyhwm2014 import HWM14, HWM14Plot    
    >>> hwm14Obj = HWM14( altlim=[90,200], altstp=1, ap=[-1, 35], day=323,
            option=1, ut=11.66667, verbose=False, year=1993 )            
    >>> hwm14Gbj = HWM14Plot( profObj=hwm14Obj )
    
    
.. image:: graphics/figure_1.png
    :scale: 100 %

You can also list the values on screen as follows

.. code-block:: bash

    >>> from pyhwm2014 import HWM14
    >>> hwm14Obj = HWM14( altlim=[90,200], altstp=10, ap=[-1, 35], day=323,
            option=1, ut=11.66667, verbose=True, year=1993 )
    
    HEIGHT PROFILE
                     quiet         disturbed             total
     alt      mer      zon      mer      zon      mer      zon
      90   11.112   28.727   -0.001   -0.000   11.112   28.726
     100   26.762    6.705   -0.007   -0.006   26.755    6.700
     110  -40.361    1.468   -0.080   -0.066  -40.442    1.402
     120  -15.063  -16.198   -0.777   -0.640  -15.840  -16.838
     130    5.352  -28.597   -2.713   -2.233    2.639  -30.829
     140   -7.310  -28.295   -3.410   -2.806  -10.720  -31.101
     150  -23.281  -26.597   -3.484   -2.867  -26.765  -29.464
     160  -34.557  -20.983   -3.490   -2.872  -38.047  -23.855
     170  -40.041  -13.405   -3.491   -2.872  -43.531  -16.277
     180  -37.589  -12.893   -3.491   -2.872  -41.080  -15.765
     190  -29.611  -18.405   -3.491   -2.872  -33.102  -21.278
     200  -19.680  -26.278   -3.491   -2.872  -23.171  -29.150


----------------------
Geog. Latitude Profile
----------------------

.. code-block:: bash
    
    >>> from pyhwm2014 import HWM14, HWM14Plot
    >>> hwm14Obj = HWM14( alt=130., ap=[-1, 35], day=323, glatlim=[-90.,90.],
            glatstp=1., option=2, ut=11.66667, verbose=False, year=1993 )            
    >>> hwm14Gbj = HWM14Plot( profObj=hwm14Obj )
    
        
.. image:: graphics/figure_2.png
    :scale: 100 %

------------------
GMT Profile
------------------

.. code-block:: bash

    >>> from pyhwm2014 import HWM14, HWM14Plot
    >>> hwm14Obj = HWM14( alt=130., ap=[-1, 35], day=323,
            option=3, utlim=[0., 23.45], utstp=.25, verbose=False, year=1993 )            
    >>> hwm14Gbj = HWM14Plot( profObj=hwm14Obj )
    

.. image:: graphics/figure_3.png
    :scale: 100 %

-----------------------
Geog. Longitude Profile
-----------------------

.. code-block:: bash

    >>> from pyhwm2014 import HWM14, HWM14Plot
    >>> hwm14Obj = HWM14( alt=130., ap=[-1, 35], day=323, glonlim=[-180., 180.], glonstp=2.,
            option=4, verbose=False, year=1993 )            
    >>> hwm14Gbj = HWM14Plot( profObj=hwm14Obj )


.. image:: graphics/figure_4.png
    :scale: 100 %

-----------------------
Height vs GMT
-----------------------

.. code-block:: bash

    >>> from pyhwm2014 import HWM142D, HWM142DPlot
    >>> hwm14Obj = HWM142D(altlim=[90,200], altstp=2, ap=[-1, 35], 
            option=1, utlim=[0.,23.75], utstp=.25, verbose=False)
    >>> hwm14Gbj = HWM142DPlot(profObj=hwm14Obj, zMin=[-75., -100], zMax=[75., 100.])

.. image:: graphics/figure_11.png
    :scale: 100 %

-------------------------
Height vs Geog. Latitude
-------------------------

.. code-block:: bash

    >>> from pyhwm2014 import HWM142D, HWM142DPlot
    >>> hwm14Obj = HWM142D(altlim=[90., 200.], altstp=2., ap=[-1, 35], 
            glatlim=[-90., 90.], glatstp=2., option=2, verbose=False, ut=12.)            
    >>> hwm14Gbj = HWM142DPlot(profObj=hwm14Obj, zMin=[-250., -100], zMax=[250., 100.])

.. image:: graphics/figure_12.png
    :scale: 100 %

-------------------------
Height vs Geog. Longitude
-------------------------

.. code-block:: bash

    >>> from pyhwm2014 import HWM142D, HWM142DPlot
    >>> hwm14Obj = HWM142D(altlim=[90., 200.], altstp=1., ap=[-1, 35], 
            glonlim=[-90., 90.], glonstp=2., option=4, ut=12., verbose=False)            
    >>> hwm14Gbj = HWM142DPlot(profObj=hwm14Obj, zMin=[-100., -100], zMax=[100., 100.])

.. image:: graphics/figure_14.png
    :scale: 100 %

----------------------------------
Geog. Latitude vs Geog. Longitude
----------------------------------

.. code-block:: bash

    >>> from pyhwm2014 import HWM142D, HWM142DPlot
    >>> hwm14Obj = HWM142D(alt=130., ap=[-1, 35], glatlim=[-90., 90.], 
            glatstp=1., glonlim=[-180., 180.], glonstp=2., option=6, verbose=False)
    >>> hwm14Gbj = HWM142DPlot(profObj=hwm14Obj, zMin=[-150., -150], zMax=[150., 150.])

.. image:: graphics/figure_16.png
    :scale: 100 %

----------------------------------
Horizontal Wind Field Map 
----------------------------------

.. code-block:: bash

    >>> from pyhwm2014 import HWM142D, HWM142DPlot
    >>> hwm14Obj = HWM142D(alt=400., ap=[-1, 35], glatlim=[-90., 90.], glatstp=10., 
            glonlim=[-180., 180.], glonstp=20., option=6, verbose=False)
    >>> hwm14Gbj = HWM142DPlot( profObj=hwm14Obj, WF=True, zMin=[-150., -150], 
            zMax=[150., 150.] )
    
.. image:: graphics/figure_16b.png
    :scale: 100 %


References
==========

.. [1] Peterson, P. `"F2PY: Fortran to Python interface generator" <https://sysbio.ioc.ee/projects/f2py2e/>`_

.. [2] Drob, D. P. et al. `"An update to the Horizontal Wind Model (HWM): The quiet time thermosphere", Earth and Space Science, 2015 <http://onlinelibrary.wiley.com/doi/10.1002/2014EA000089/full>`_

---------------------
Wrapping Fortran code
---------------------
This is for reference, no need to do this as it's done by  ``python setup.py develop``

1. The first step is to ask 'f2py' to write the signature of the routine (hwm14.f90) to 
a description file

.. code-block:: bash

    $ f2py hwm14.f90 -m hwm14 -h hwm14.pyf
    
The '-m' flag gives the name the python module should have (hwm14). The '-h' flag tells 
'f2py' in which file should write the signature (see file 'hwm14.pyf').

2. 'f2py' recognizes which variables need to be passed in or out. This is done by the command 
'intent' added to the declaration of variables. 

3. Now everything is ready and the module can be compiled. f2py will try to find a compiler 
in your path and use it. So all to be typed is

.. code-block:: bash

    $ f2py -c hwm14.pyf hwm14.f90

'f2py' will write the wrapper files, compile hwm14.f90 and the wrapper files, and link them 
in a shared object. After this step, one can start Python and load the extension module.

NOTE: To specify a Fortran compiler type by vendor, e.g. ifort (Intel Fortran compiler):

.. code-block:: bash

    $ f2py -c hwm14.pyf hwm14.f90 --fcompiler=intelem

