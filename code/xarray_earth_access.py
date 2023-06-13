import os
import xarray as xr
import matplotlib.pyplot as plt
import earthaccess

granules = []
home_dir = os.path.expanduser('~')

auth = earthaccess.login(strategy="netrc", persist=True)

# we just grab 1 granule from May for each year of the dataset
for year in range(1990, 2019):
    granule = earthaccess.granule_query().short_name("SEA_SURFACE_HEIGHT_ALT_GRIDS_L4_2SATS_5DAY_6THDEG_V_JPL2205").temporal(f"{year}-05", f"{year}-06").get(1)
    if len(granule)>0:
        granules.append(granule[0])
print(f"Total granules: {len(granules)}")

ds = xr.open_mfdataset(earthaccess.open(granules), chunks={})
plot = ds.SLA.where((ds.SLA>=0) & (ds.SLA < 10)).std('Time').plot(figsize=(14,6), x='Longitude', y='Latitude')
home_dir = os.path.expanduser('~')
plot.figure.savefig(os.path.join(home_dir, 'sla_plot.png'))

