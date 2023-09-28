# ---
# jupyter:
#   jupytext:
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Component FDTD simulations
#
# Thanks to the GDSFactory plugin you can directly run simulations in different FDTD solvers.
#
# See [tutorial](https://gdsfactory.github.io/gdsfactory/plugins_fdtd.html)

# ## Tidy3d
#
# You can read about the [tidy3d gdsfactory plugin](https://gdsfactory.github.io/gdsfactory/notebooks/plugins/tidy3d/00_tidy3d.html)

# +
import gplugins as sim
import gplugins.tidy3d as gt

import ubcpdk.components as pdk
from ubcpdk.config import PATH

# -

c = pdk.ebeam_y_1550()
c.plot()

sp = gt.write_sparameters(c, filepath=PATH.sparameters / "ebeam_y_1550_20634f71.npz")

sp.keys()

sim.plot.plot_sparameters(sp)

sim.plot.plot_loss1x2(sp)

sim.plot.plot_imbalance1x2(sp)

# ## Lumerical FDTD
#
# You can write the [Sparameters](https://en.wikipedia.org/wiki/Scattering_parameters) for all components in the UBC `ubcpdk.components` PDK using lumerical FDTD plugin in gplugins

# To run simulations uncomment the following lines

# +
import gplugins as sim

import ubcpdk.components as pdk

# -

for f in [
    pdk.bend_euler,
    pdk.coupler,
    pdk.coupler_ring,
    pdk.ebeam_y_1550,
    pdk.ebeam_crossing4,
]:
    component = f()
    component.plot_klayout()
    # ls.write_sparameters_lumerical(component=component)


# +
# sp = ls.read.read_sparameters_lumerical(component=ubcpdk.components.straight())

# +
# sim.plot_sparameters(sp)
