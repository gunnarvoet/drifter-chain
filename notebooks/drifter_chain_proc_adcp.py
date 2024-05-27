# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python [conda env:drifter]
#     language: python
#     name: conda-env-drifter-py
# ---

# %% [markdown]
# # Drifter Chain ADCP Processing

# %%
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
import gsw
import gvpy as gv
import velosearaptor

# %reload_ext autoreload
# %autoreload 2
# %config InlineBackend.figure_format = 'retina'

# %%
data_path = Path("/Users/gunnar/Projects/nesma/drifter/data/drifter_chain_2024_05")

# %% [markdown] jp-MarkdownHeadingCollapsed=true
# ## 1-Day Test

# %%
ncstr_1_day_test = "drifter_tchain_2024_05_13_adcp_3160"
raw_file = data_path.joinpath("adcp/raw/03160000.000")

# %%
raw = velosearaptor.io.read_raw_rdi(raw_file)

# %%
raw_out = data_path.joinpath(f"adcp/proc/{ncstr_1_day_test}_raw.nc")
raw.to_netcdf(raw_out, encoding={
    "time": {"units": "seconds since 1970-01-01", "dtype": "float"},
    })

# %% [markdown]
# Plot raw data

# %%
velosearaptor.adcp.plot_raw_adcp(raw)
fig_out = data_path.joinpath(f"adcp/fig/{ncstr_1_day_test}_raw")
gv.plot.png(fig_out)

# %%
velosearaptor.adcp.plot_raw_adcp_auxillary(raw)

# %% [markdown]
# Process raw-data

# %%
meta_data = dict(lon=-130, lat=30, mooring=ncstr_1_day_test, sn=3160)
tgridparams = dict(dt_hours=3/60)
a = velosearaptor.madcp.ProcessADCP(raw_file, meta_data=meta_data, tgridparams=tgridparams)

# %%
a.plot_echo_stats()

# %%
a.average_ensembles()

# %% [markdown]
# Save to netcdf

# %%
proc_out = data_path.joinpath(f"adcp/proc/{ncstr_1_day_test}.nc")
a.ds.to_netcdf(proc_out, encoding={
    "time": {"units": "seconds since 1970-01-01", "dtype": "float"},
    })

# %% [markdown]
# A few plots

# %%
a.ds.pg.gv.plot()

# %%
a.ds.amp.gv.plot()

# %%
fig, ax = gv.plot.quickfig(r=5, sharex=True, fgs=(8, 8), grid=True)
a.ds.u.gv.plot(cmap="RdBu_r", vmin=-0.1, vmax=0.1, ax=ax[0])
a.ds.v.gv.plot(cmap="RdBu_r", vmin=-0.1, vmax=0.1, ax=ax[1])
a.ds.w.gv.plot(robust=True, ax=ax[2])
a.ds.xducer_depth.gv.plot(ax=ax[2], color="k")
# sbe.p.gv.plot(ax=ax[2], color="0.3", linestyle="--")
ax[2].set(ylabel="depth [m]")

a.ds.u.differentiate("depth").gv.plot(
    cmap="RdBu_r",
    vmin=-0.01,
    vmax=0.01,
    ax=ax[3],
    cbar_kwargs=dict(label="u$_z$ [s$^{-1}$]"),
)
a.ds.v.differentiate("depth").gv.plot(
    cmap="RdBu_r",
    vmin=-0.01,
    vmax=0.01,
    ax=ax[4],
    cbar_kwargs=dict(label="v$_z$ [s$^{-1}$]"),
)
for axi in ax:
    axi.grid()

fig_out = data_path.joinpath(f"adcp/fig/{ncstr_1_day_test}_vel_and_shear")
gv.plot.png(fig_out)

# %% [markdown]
# ## 2-Day Test

# %%
ncstr_2_day_test = "drifter_tchain_2024_05_17_adcp_3160"
raw_file = data_path.joinpath("adcp/raw/03160002.000")

# %%
raw = velosearaptor.io.read_raw_rdi(raw_file)

# %% [markdown]
# Save raw data to netcdf

# %%
raw_out = data_path.joinpath(f"adcp/proc/{ncstr_2_day_test}_raw.nc")
raw.to_netcdf(raw_out, encoding={
    "time": {"units": "seconds since 1970-01-01", "dtype": "float"},
    })

# %% [markdown]
# Plot raw data

# %%
velosearaptor.adcp.plot_raw_adcp(raw)
fig_out = data_path.joinpath(f"adcp/fig/{ncstr_2_day_test}_raw")
gv.plot.png(fig_out)

# %%
velosearaptor.adcp.plot_raw_adcp_auxillary(raw)

# %% [markdown]
# Process raw-data

# %%
meta_data = dict(lon=-130, lat=30, mooring=ncstr_2_day_test, sn=3160)
tgridparams = dict(dt_hours=3/60)
a = velosearaptor.madcp.ProcessADCP(raw_file, meta_data=meta_data, tgridparams=tgridparams)

# %%
a.plot_echo_stats()

# %%
binmask = a.generate_binmask(0)

# %%
a.editparams["maskbins"] = binmask

# %%
a.average_ensembles()

# %% [markdown]
# Save to netcdf

# %%
proc_out = data_path.joinpath(f"adcp/proc/{ncstr_2_day_test}.nc")
a.ds.to_netcdf(proc_out, encoding={
    "time": {"units": "seconds since 1970-01-01", "dtype": "float"},
    })

# %% [markdown]
# A few plots

# %%
a.ds.pg.gv.plot()

# %%
a.ds.amp.gv.plot()

# %%
fig, ax = gv.plot.quickfig(r=5, sharex=True, fgs=(8, 8), grid=True)
a.ds.u.gv.plot(cmap="RdBu_r", vmin=-0.1, vmax=0.1, ax=ax[0])
a.ds.v.gv.plot(cmap="RdBu_r", vmin=-0.1, vmax=0.1, ax=ax[1])
a.ds.w.gv.plot(robust=True, ax=ax[2])
a.ds.xducer_depth.gv.plot(ax=ax[2], color="k")
# sbe.p.gv.plot(ax=ax[2], color="0.3", linestyle="--")
ax[2].set(ylabel="depth [m]")

a.ds.u.differentiate("depth").gv.plot(
    cmap="RdBu_r",
    vmin=-0.01,
    vmax=0.01,
    ax=ax[3],
    cbar_kwargs=dict(label="u$_z$ [s$^{-1}$]"),
)
a.ds.v.differentiate("depth").gv.plot(
    cmap="RdBu_r",
    vmin=-0.01,
    vmax=0.01,
    ax=ax[4],
    cbar_kwargs=dict(label="v$_z$ [s$^{-1}$]"),
)
for axi in ax:
    axi.grid()

fig_out = data_path.joinpath(f"adcp/fig/{ncstr_2_day_test}_vel_and_shear")
gv.plot.png(fig_out)

# %%
tmp = a.ds.sel(time=slice("2024-05-19 00:00", "2024-05-19 12:00"))
fig, ax = gv.plot.quickfig(r=3, sharex=True, fgs=(8, 8), grid=True)
tmp.u.gv.plot(cmap="RdBu_r", vmin=-0.1, vmax=0.1, ax=ax[0])
tmp.v.gv.plot(cmap="RdBu_r", vmin=-0.1, vmax=0.1, ax=ax[1])
tmp.w.gv.plot(robust=True, ax=ax[2])
tmp.xducer_depth.gv.plot(ax=ax[2], color="k")
# sbe.p.gv.plot(ax=ax[2], color="0.3", linestyle="--")
ax[2].set(ylabel="depth [m]")

for axi in ax:
    axi.grid()

# %%
tmp = a.ds.sel(time=slice("2024-05-18 00:00", "2024-05-19 12:00"))
fig, ax = gv.plot.quickfig(r=1, sharex=True, fgs=(10, 3), grid=True)
tmp.w.gv.plot(robust=True, ax=ax)
tmp.xducer_depth.gv.plot(ax=ax, color="k")
ax.set(ylabel="depth [m]", ylim=(220, 0))
ax.grid()

# %% [markdown]
# Zoom into first drift

# %%
mask = (a.ds.pressure > 180) & (a.ds.time < np.datetime64("2024-05-19 20:00"))

# %%
a.ds.pressure[mask].plot()

# %%
aa = a.ds.sel(time=mask)
# aa = aa.where(aa.pg>50)
# aa = aa.dropna(dim="depth", how="all")
aa = aa.dropna(dim="depth")

# %%
aa.w.gv.plot(robust=True)

# %%
ax = aa.u.mean("time").gv.plot()
ax = aa.v.mean("time").gv.plot(ax=ax)

# %%
aa.pg.gv.plot()

# %%
