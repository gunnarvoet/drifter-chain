from pathlib import Path
import rbrmoored

data = Path("/Users/gunnar/Projects/nesma/data/drifter_thermistors/")
files = sorted(data.glob("*.rsk"))

data_out = Path.cwd() / "nc"
fig_out = Path.cwd() / "fig"

for file in files:
    t = rbrmoored.solo.proc(file, data_out=data_out, figure_out=fig_out, show_plot=True)
