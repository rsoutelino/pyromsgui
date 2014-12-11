pyromsgui
=========

GUI to view ROMS input/output files. Still unstable, lots on the to-do list, lots of functionality still to come. Help is welcome, fork encouraged. 

- Requires internet connection
- Default install location is `yourpythonpath/lib/site-packages/`
- Dependencies: `wxpython, numpy, scipy, matplotlib, netCDF4`

Manual install
----
```
git clone https://github.com/rsoutelino/pyromsgui.git
cd pyromsgui
python setup.py install
```

Installing from pypy
----
```
pip install pyromsgui
```

Executing
----
```
python yourpyromsguipath/pyromsgui.py
```

Usage cases
----
- **Plotting horizontal slices**: Load a ROMS his/ini/clm and grd netcdf files using the far left toolbar buttom. Default plots bathymetry. Use left panel menus to navigate between variables and time stamps. 
- **Plotting vertical slices**: Choose a "sliceable" 3D variable. Toggle the brown *vslice* buttom, click in the desired start and end points for the vertical slice. On the pop-up window, chose your plot type, color range, etc. 

