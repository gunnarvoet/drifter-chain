# %% [markdown]
# # Drifter Chain RBR Solo Processing

# %%
from pathlib import Path
import numpy as np
import rbrmoored
import xarray as xr
import gvpy as gv

# %reload_ext autoreload
# %autoreload 2
# %config InlineBackend.figure_format = 'retina'

# %% [markdown]
# The time offset for the RBR Solo has been recorded with a computer set to local time, need to adjust the time drift parameter by 7 hours.

# %% [markdown]
# SN 230754 and SN 230757 do not show a download time and thus also no time drift.

# %% [markdown]
# ---

# %% [markdown]
# Set up paths

# %%
rbr_data_dir = Path("/Users/gunnar/Projects/nesma/drifter/data/drifter_chain_2024_05/rbrsolo/")
data_raw_dir = rbr_data_dir.joinpath("raw")
files = sorted(data_raw_dir.glob("*.rsk"))

# %%
data_proc_dir = rbr_data_dir.joinpath("proc")
fig_dir = rbr_data_dir.joinpath("fig")

# %% [markdown]
# Process all files

# %%
if False:
    for file in files:
        t = rbrmoored.solo.proc(
            file, data_out=data_proc_dir, figure_out=fig_dir, show_plot=True, offset_time_drift=7
        )

# %% [markdown]
# Re-process SN 230757 (initial download was only partial).

# %%
file = files[-1]
file

# %%
t = rbrmoored.solo.proc(
    file, data_out=data_proc_dir, figure_out=fig_dir, show_plot=True, offset_time_drift=0
)

# %%
# manually reading time drift from clock cal (see plot below)
t.attrs["time drift in ms"] = 1.2e3
# correct for time drift
t = rbrmoored.solo.time_offset(t)

# %%
# save
t.gv.to_netcdf(data_proc_dir.joinpath(file.stem), overwrite=True)

# %%
t = rbrmoored.solo.proc(
    file, data_out=data_proc_dir, figure_out=fig_dir, show_plot=True, offset_time_drift=0
)

# %% [markdown]
# Adjust time vector SN 230754

# %%
file = data_proc_dir.joinpath("230754_20240522_2214.nc")
t = xr.open_dataarray(file)

# %%
# manually reading time drift from clock cal (see plot below)
t.attrs["time drift in ms"] = 200
# correct for time drift
t = rbrmoored.solo.time_offset(t)

# %%
# save
t.gv.to_netcdf(file, overwrite=True)

# %%
t = rbrmoored.solo.proc(
    data_raw_dir.joinpath("230754_20240522_2214.rsk"), data_out=data_proc_dir, figure_out=fig_dir, show_plot=True, offset_time_drift=0
)

# %% [markdown]
# ---

# %% [markdown]
# Read all files.

# %%
files_nc = sorted(data_proc_dir.glob("*.nc"))

# %%
allt = [xr.open_dataarray(file) for file in files_nc]

# %%
fig, ax = gv.plot.quickfig()
for ti in allt:
    ti.gv.plot(ax=ax)
ax.grid()

# %%
ts = slice("2024-05-17", "2024-05-22")
tt = [ti.sel(time=ts) for ti in allt]

# %%
fig, ax = gv.plot.quickfig()
for ti in tt:
    ti.gv.plot(ax=ax)
ax.grid()

# %% [markdown]
# Plot clock calibration - everything within 1s. The one outlier may be the one that displayed a funky time offset.

# %%
ts_dip = slice("2024-05-22 20:27:20", "2024-05-22 20:27:40")
fig, ax = gv.plot.quickfig()
for ti in tt:
    ti.sel(time=ts_dip).gv.plot(ax=ax, color="k", alpha=0.5, linewidth=1)
ax.grid()
gv.plot.png(
    "/Users/gunnar/Projects/nesma/drifter/data/drifter_chain_2024_05/rbrsolo/fig/clock_verification"
)

# %%
ts_dip = slice("2024-05-18", "2024-05-19 18:00")
fig, ax = gv.plot.quickfig()
for ti in tt:
    ti.sel(time=ts_dip).gv.plot(ax=ax)
ax.grid()

# %%
