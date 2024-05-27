from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr


nc_dir = Path("nc/")

nc_files = nc_dir.glob("*.nc")

t_all = [xr.open_dataarray(file) for file in nc_files]

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7.5, 5),
                       constrained_layout=True)
[ti.plot(ax=ax) for ti in t_all]
