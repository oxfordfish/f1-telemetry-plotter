from pathlib import Path
import fastf1
from fastf1 import plotting
import matplotlib.pyplot as plt
import numpy as np

# Configure FastF1 styling & caching
plotting.setup_mpl()

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

# Session config
YEAR = 2023
GRAND_PRIX = "Monaco"
SESSION_TYPE = "Q"
DRIVER_1, DRIVER_2 = "VER", "LEC"


def main():
    print(f"Fetching {YEAR} {GRAND_PRIX} GP ({SESSION_TYPE}) data...")
    session = fastf1.get_session(YEAR, GRAND_PRIX, SESSION_TYPE)
    session.load()

    # Get fastest laps and telemetry
    lap_1 = session.laps.pick_driver(DRIVER_1).pick_fastest()
    lap_2 = session.laps.pick_driver(DRIVER_2).pick_fastest()

    tel_1 = lap_1.get_telemetry()
    tel_2 = lap_2.get_telemetry()

    c1 = plotting.get_driver_color(DRIVER_1, session=session)
    c2 = plotting.get_driver_color(DRIVER_2, session=session)

    # ------------------------------------
    # Telemetry Traces
    # ------------------------------------
    channels = [
        ("Speed", "Speed (km/h)"),
        ("Throttle", "Throttle %"),
        ("Brake", "Brake"),
        ("nGear", "Gear"),
    ]

    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    fig.suptitle(
        f"{YEAR} {GRAND_PRIX} GP ({SESSION_TYPE}) — {DRIVER_1} vs {DRIVER_2}",
        fontsize=14,
        fontweight="bold",
    )

    for ax, (channel, label) in zip(axes, channels):
        ax.plot(
            tel_1["Distance"],
            tel_1[channel],
            color=c1,
            label=f"{DRIVER_1} ({lap_1['LapTime']})",
        )
        ax.plot(
            tel_2["Distance"],
            tel_2[channel],
            color=c2,
            label=f"{DRIVER_2} ({lap_2['LapTime']})",
        )
        ax.set_ylabel(label)
        ax.grid(True, linestyle="--", alpha=0.5)

    # Handle single legend on top plot to avoid redundancy
    axes[0].legend(loc="lower right")
    axes[-1].set_xlabel("Distance (m)")

    plt.tight_layout()
    plt.savefig("telemetry_comparison.png", dpi=300)
    print("Exported telemetry_comparison.png")

    # ------------------------------------
    # Speed Map
    # ------------------------------------
    x, y, speed = tel_1["X"].to_numpy(), tel_1["Y"].to_numpy(), tel_1["Speed"].to_numpy()

    fig_map, ax_map = plt.subplots(figsize=(10, 8))
    ax_map.axis("off")

    sc = ax_map.scatter(x, y, c=speed, cmap="plasma", s=8)
    cbar = fig_map.colorbar(sc, ax=ax_map, orientation="horizontal", pad=0.05)
    cbar.set_label("Speed (km/h)", fontsize=11)

    ax_map.set_title(
        f"{GRAND_PRIX} Circuit Speed Map — {DRIVER_1}", fontsize=14, fontweight="bold"
    )

    plt.tight_layout()
    plt.savefig("track_map.png", dpi=300)
    print("Exported track_map.png")


if __name__ == "__main__":
    main()
