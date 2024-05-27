# %% [markdown]
# # Drifter Chain SBE56 Processing

# %%
from pathlib import Path
import numpy as np
import sbemoored
import xarray as xr
import gvpy as gv

# %reload_ext autoreload
# %autoreload 2
# %config InlineBackend.figure_format = 'retina'

# %%
sbe56_data_dir = Path("/Users/gunnar/Projects/nesma/drifter/data/drifter_chain_2024_05/sbe56/")
data_raw_dir = sbe56_data_dir.joinpath("raw")
files = sorted(data_raw_dir.glob("*.csv"))

# %%
data_proc_dir = sbe56_data_dir.joinpath("proc")
fig_dir = sbe56_data_dir.joinpath("fig")

# %%
tmpf = files[0]
tmpf

# %%
t = sbemoored.sbe56.proc(tmpf, data_out=data_proc_dir, figure_out=fig_dir)

# %% [markdown]
# Process all files.

# %%
if None:
    for file in files:
        t = sbemoored.sbe56.proc(file, data_out=data_proc_dir, figure_out=fig_dir)

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
# Plot clock calibration - everything within 2s.

# %%
ts_dip = slice("2024-05-22 20:26:20", "2024-05-22 20:26:40")
fig, ax = gv.plot.quickfig()
for ti in tt:
    ti.sel(time=ts_dip).gv.plot(ax=ax, color="k", alpha=0.5, linewidth=1)
ax.grid()
gv.plot.png(fig_dir.joinpath("clock_verification.png"))

# %% [markdown]
# Sampling period was 1 Hz.

# %%
allt[0].gv.sampling_period

# %%
ts_dip = slice("2024-05-18", "2024-05-19 18:00")
fig, ax = gv.plot.quickfig()
for ti in tt:
    ti.sel(time=ts_dip).gv.plot(ax=ax)
ax.grid()

# %%
