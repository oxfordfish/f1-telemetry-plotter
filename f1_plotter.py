import os
import fastf1
from fastf1 import plotting
import matplotlib.pyplot as plt
import numpy as np

# 1. Setup FastF1 styling & local caching folder
plotting.setup_mpl()

cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
fastf1.Cache.enable_cache(cache_dir)

print("Fetching session data from FastF1...")

# 2. Load Session (e.g., 2023 Monaco GP Qualifying)
YEAR = 2023
GRAND_PRIX = 'Monaco'
SESSION_TYPE = 'Q'

session = fastf1.get_session(YEAR, GRAND_PRIX, SESSION_TYPE)
session.load()

# 3. Select Fastest Laps
driver1 = 'VER'
driver2 = 'LEC'

lap_1 = session.laps.pick_driver(driver1).pick_fastest()
lap_2 = session.laps.pick_driver(driver2).pick_fastest()

# Get Telemetry
tel_1 = lap_1.get_telemetry()
tel_2 = lap_2.get_telemetry()

# Get Driver Colors
color_1 = fastf1.plotting.get_driver_color(driver1, session=session)
color_2 = fastf1.plotting.get_driver_color(driver2, session=session)

# ---------------------------------------------------------
# FIGURE 1: TELEMETRY TRACES
# ---------------------------------------------------------
fig, ax = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
fig.suptitle(f"{YEAR} {GRAND_PRIX} GP ({SESSION_TYPE}) - {driver1} vs {driver2} Telemetry", fontsize=14, fontweight='bold')

# Speed
ax[0].plot(tel_1['Distance'], tel_1['Speed'], label=f"{driver1} ({lap_1['LapTime']})", color=color_1)
ax[0].plot(tel_2['Distance'], tel_2['Speed'], label=f"{driver2} ({lap_2['LapTime']})", color=color_2)
ax[0].set_ylabel('Speed (km/h)')
ax[0].legend(loc='lower right')
ax[0].grid(True, linestyle='--', alpha=0.5)

# Throttle
ax[1].plot(tel_1['Distance'], tel_1['Throttle'], color=color_1)
ax[1].plot(tel_2['Distance'], tel_2['Throttle'], color=color_2)
ax[1].set_ylabel('Throttle %')
ax[1].grid(True, linestyle='--', alpha=0.5)

# Brake
ax[2].plot(tel_1['Distance'], tel_1['Brake'], color=color_1)
ax[2].plot(tel_2['Distance'], tel_2['Brake'], color=color_2)
ax[2].set_ylabel('Brake')
ax[2].grid(True, linestyle='--', alpha=0.5)

# Gear
ax[3].plot(tel_1['Distance'], tel_1['nGear'], color=color_1)
ax[3].plot(tel_2['Distance'], tel_2['nGear'], color=color_2)
ax[3].set_ylabel('Gear')
ax[3].set_xlabel('Distance (m)')
ax[3].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('telemetry_comparison.png', dpi=300)
print("Saved telemetry_comparison.png!")

# ---------------------------------------------------------
# FIGURE 2: SPEED-COLORED TRACK MAP
# ---------------------------------------------------------
x = tel_1['X'].to_numpy()
y = tel_1['Y'].to_numpy()
speed = tel_1['Speed'].to_numpy()

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

fig_map, ax_map = plt.subplots(figsize=(10, 8))
ax_map.axis('off')

# Scatter plot colored by speed for a clean track rendering
lc = ax_map.scatter(x, y, c=speed, cmap='plasma', s=8)
cbar = fig_map.colorbar(lc, ax=ax_map, orientation='horizontal', pad=0.05)
cbar.set_label('Speed (km/h)', fontsize=12)

ax_map.set_title(f"{GRAND_PRIX} Circuit Map - {driver1} Speed Profile", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('track_map.png', dpi=300)
print("Saved track_map.png!")

plt.show()

