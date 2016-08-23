======
pyHWM14
======
Python interface for the Horizontal Wind Model version 14

.. contents::

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

NOTE:
- To specify a Fortran compiler type by vendor, e.g. ifort (Intel Fortran compiler):

.. code-block:: bash

    $ f2py -c hwm14.pyf hwm14.f90 --fcompiler=intelem

Examples
========

--------------
Height Profile
--------------

.. code-block:: bash

    import pyhwm14
    hwm14Obj = pyhwm14.HWM14( option=1, verbose=False )
    hwm14Gbj = pyhwm14.HWM14Plot( profObj=hwm14Obj )
    
.. image:: graphics/figure_1.png
    :scale: 100 %

----------------------
Geog. Latitude Profile
----------------------

.. code-block:: bash

    import pyhwm14
    hwm14Obj = pyhwm14.HWM14( option=2, verbose=False )
    hwm14Gbj = pyhwm14.HWM14Plot( profObj=hwm14Obj )
    
.. image:: graphics/figure_2.png
    :scale: 100 %

------------------
Local Time Profile
------------------

.. code-block:: bash

    import pyhwm14
    hwm14Obj = pyhwm14.HWM14( option=3, verbose=False )
    hwm14Gbj = pyhwm14.HWM14Plot( profObj=hwm14Obj )

.. image:: graphics/figure_3.png
    :scale: 100 %

-----------------------
Geog. Longitude Profile
-----------------------

.. code-block:: bash

    import pyhwm14
    hwm14Obj = pyhwm14.HWM14( option=4, verbose=False )
    hwm14Gbj = pyhwm14.HWM14Plot( profObj=hwm14Obj )

.. image:: graphics/figure_4.png
    :scale: 100 %

References
==========
.. [1] Drob, D. P. et al. `"An update to the Horizontal Wind Model (HWM): The quiet time thermosphere", Earth and Space Science, 2015 <http://onlinelibrary.wiley.com/doi/10.1002/2014EA000089/full>`_
