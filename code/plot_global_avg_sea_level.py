import os
import numpy as np
from pyproj import Geod
from matplotlib import pyplot as plt
import earthaccess
import xarray as xr

auth = earthaccess.login(strategy="netrc", persist=True)

granules = []

for year in range(1990, 2019):
    granule = earthaccess.granule_query().short_name("SEA_SURFACE_HEIGHT_ALT_GRIDS_L4_2SATS_5DAY_6THDEG_V_JPL2205").temporal(f"{year}-05", f"{year}-06").get(1)
    if len(granule)>0:
        granules.append(granule[0])
print(f"Total granules: {len(granules)}")

def ssl_area(lats):
    # Define WGS84 as CRS:
    geod = Geod(ellps='WGS84')
    dx=1/12.0
    c_area=lambda lat: geod.polygon_area_perimeter(np.r_[-dx,dx,dx,-dx], lat+np.r_[-dx,-dx,dx,dx])[0]
    out=[]
    for lat in lats:
        out.append(c_area(lat))
    return np.array(out)
ds = xr.open_mfdataset(earthaccess.open(granules), chunks={})

ssh_area = ssl_area(ds.Latitude.data).reshape(-1,1)
print(ssh_area.shape)

plt.rcParams["figure.figsize"] = (16,4)

# Create a blank image with the desired dimensions
blank_img = np.ones((100, 100, 3))  # Adjust the dimensions as needed

fig, axs = plt.subplots()
plt.grid(True)

def global_mean(SLA, **kwargs):
    dout=((SLA*ssh_area).sum()/(SLA/SLA*ssh_area).sum())*1000
    return dout

result = ds.SLA.groupby('Time').apply(global_mean)

plt.xlabel('Time (year)',fontsize=16)
plt.ylabel('Global Mean SLA (meter)',fontsize=12)
# axs.imshow(img, aspect='auto')
plt.grid(True)



#historic_ts=xr.open_dataset('https://opendap.jpl.nasa.gov/opendap/allData/homage/L4/gmsl/global_timeseries_measures.nc')

result.plot(ax=axs, color="orange", marker="o", label='satellite record')

#historic_ts['global_average_sea_level_change'].plot(ax=axs, label='Historical in-situ record', color="lightblue")

# Use the blank image as the background
#x0, x1 = axs.get_xlim()
#y0, y1 = axs.get_ylim()
# axs.imshow(blank_img, extent=[x0, x1, y0, y1], aspect='auto')

plt.legend()
home_dir = os.path.expanduser('~')
fig.figure.savefig(os.path.join(home_dir, 'global_sea_level_avg.png'))
exit(0)
print('end of workflow run')

