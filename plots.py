# plots.py

import matplotlib.pyplot as plt
import numpy as np

def plot_beam_diagram(beam):
    """
    Draw a simple schematic: the beam as a horizontal line,
    supports as markers, point loads as arrows, UDLs as arrow‐arrays.
    """
    fig, ax = plt.subplots(figsize=(6, 2))
    # Beam line
    ax.hlines(0, 0, beam.length, colors='black', linewidth=4)

    # Supports
    for sup in beam.supports:
        x = sup["pos"]
        if sup["type"] == "pin":
            marker = "^"
        else:
            marker = "o"
        ax.plot(x, 0, marker=marker, markersize=12, color="blue")

    # Point loads
    for pl in beam.point_loads:
        x, P = pl["pos"], pl["mag"]
        # arrow up at top of beam
        ax.arrow(x, 0.3, 0, -0.25, head_width=0.1, head_length=0.05, length_includes_head=True)
        ax.text(x, 0.35, f"{P:.1f} kN", ha="center")

    # UDLs
    for udl in beam.distributed_loads:
        xs = np.linspace(udl["start"], udl["end"], 10)
        for xi in xs:
            ax.arrow(xi, 0.2, 0, -0.15, head_width=0.05, head_length=0.03, length_includes_head=True)
        mid = 0.5 * (udl["start"] + udl["end"])
        ax.text(mid, 0.25, f"{udl['int']:.1f} kN/m", ha="center")

    ax.set_xlim(-0.1 * beam.length, 1.1 * beam.length)
    ax.set_ylim(-0.5, 0.6)
    ax.axis("off")
    fig.tight_layout()
    return fig

def plot_sfd(beam, num=200):
    """
    Plot Shear Force Diagram V(x) over [0, length].
    """
    xs = np.linspace(0, beam.length, num)
    Vs = [beam.shear_at(x) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, Vs, linewidth=2)
    ax.fill_between(xs, Vs, 0, where=(np.array(Vs) >= 0), alpha=0.3)
    ax.fill_between(xs, Vs, 0, where=(np.array(Vs) <= 0), alpha=0.3)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Shear V(x) [kN]")
    ax.set_xlabel("x [m]")
    ax.set_title("Shear Force Diagram")
    fig.tight_layout()
    return fig

def plot_bmd(beam, num=200):
    """
    Plot Bending Moment Diagram M(x) over [0, length].
    """
    xs = np.linspace(0, beam.length, num)
    Ms = [beam.moment_at(x) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, Ms, linewidth=2)
    ax.fill_between(xs, Ms, 0, where=(np.array(Ms) >= 0), alpha=0.3)
    ax.fill_between(xs, Ms, 0, where=(np.array(Ms) <= 0), alpha=0.3)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Moment M(x) [kN·m]")
    ax.set_xlabel("x [m]")
    ax.set_title("Bending Moment Diagram")
    fig.tight_layout()
    return fig
