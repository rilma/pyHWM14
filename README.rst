======
pyHWM14
======
Python interface for the Horizontal Wind Model version 2014 (HWM14)

.. contents::

Installation
============

.. code-block:: bash

    >>> python setup.py install

Examples
========

--------------
Height Profile
--------------

.. code-block:: bash

    >>> from pyhwm2014.pyhwm14 import HWM14, HWM14Plot
    >>> hwm14Obj = HWM14( option=1, verbose=False )
    >>> hwm14Gbj = HWM14Plot( profObj=hwm14Obj )    
    
.. image:: graphics/figure_1.png
    :scale: 100 %

You can also list the values on screen as follows

.. code-block:: bash

    >>> from pyhwm2014.pyhwm14 import HWM14
    >>> hwm14Obj = HWM14( option=1, verbose=True )
    HEIGHT PROFILE
                     quiet         disturbed             total
     alt      mer      zon      mer      zon      mer      zon
       0    0.031    6.271    0.000   -0.000    0.031    6.271
      25    2.965   25.115    0.000   -0.000    2.965   25.115
      50   -6.627   96.343    0.000   -0.000   -6.627   96.343
      75    2.238   44.845    0.000   -0.000    2.238   44.845
     100  -14.339   31.627    0.086   -0.037  -14.253   31.590
     125   15.125   21.110   22.279   -9.483   37.403   11.628
     150   -1.683  -14.391   44.472  -18.929   42.789  -33.319
     175  -24.280  -31.019   44.558  -18.965   20.278  -49.984
     200  -19.531  -49.623   44.558  -18.965   25.027  -68.588
     225  -10.261  -61.057   44.558  -18.965   34.297  -80.022
     250   -4.150  -68.595   44.558  -18.965   40.408  -87.560
     275   -0.122  -73.564   44.558  -18.965   44.436  -92.530
     300    2.534  -76.840   44.558  -18.965   47.092  -95.806
     325    4.285  -79.000   44.558  -18.965   48.843  -97.965
     350    5.439  -80.424   44.558  -18.965   49.997  -99.389
     375    6.200  -81.362   44.558  -18.965   50.758 -100.327
     400    6.702  -81.981   44.558  -18.965   51.259 -100.946

----------------------
Geog. Latitude Profile
----------------------

.. code-block:: bash
    
    >>> from pyhwm2014.pyhwm14 import HWM14, HWM14Plot
    >>> hwm14Obj = HWM14( option=2, verbose=False )
    >>> hwm14Gbj = HWM14Plot( profObj=hwm14Obj )
        
.. image:: graphics/figure_2.png
    :scale: 100 %

------------------
Local Time Profile
------------------

.. code-block:: bash

    >>> from pyhwm2014.pyhwm14 import HWM14, HWM14Plot
    >>> hwm14Obj = HWM14( option=3, verbose=False )
    >>> hwm14Gbj = HWM14Plot( profObj=hwm14Obj )

.. image:: graphics/figure_3.png
    :scale: 100 %

-----------------------
Geog. Longitude Profile
-----------------------

.. code-block:: bash

    >>> from pyhwm2014.pyhwm14 import HWM14, HWM14Plot
    >>> hwm14Obj = HWM14( option=4, verbose=False )
    >>> hwm14Gbj = HWM14Plot( profObj=hwm14Obj )

.. image:: graphics/figure_4.png
    :scale: 100 %

Wrapping Fortran code
=====================

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

References
==========

.. [1] Peterson, P. `"F2PY: Fortran to Python interface generator" <https://sysbio.ioc.ee/projects/f2py2e/>`_

.. [2] Drob, D. P. et al. `"An update to the Horizontal Wind Model (HWM): The quiet time thermosphere", Earth and Space Science, 2015 <http://onlinelibrary.wiley.com/doi/10.1002/2014EA000089/full>`_
