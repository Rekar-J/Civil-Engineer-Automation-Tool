# plots.py

import numpy as np
import matplotlib.pyplot as plt

def plot_beam_diagram(beam):
    """
    Draws:
      - A horizontal beam line
      - Pin (▼) and roller (○) supports
      - Downward arrows for point loads
      - Shaded regions and arrows for UDLs
    """
    fig, ax = plt.subplots()
    L = beam.length

    # 1) Beam line
    ax.hlines(0, 0, L, linewidth=4)

    # 2) Supports
    for pos, sup_type in beam.supports:
        if sup_type == "pin":
            ax.plot(pos, 0, marker="v", markersize=15)
        else:  # roller
            ax.plot(pos, 0, marker="o", markersize=12)

    # 3) Point loads (downward)
    for px, pm in beam.point_loads:
        ax.annotate(
            "", xy=(px, -0.3), xytext=(px, 0.2),
            arrowprops=dict(arrowstyle="->", lw=2)
        )
        ax.text(px, -0.35, f"{pm:.1f} kN", ha="center", va="top")

    # 4) UDLs: arrows + shaded region + label
    for s, e, w in beam.dist_loads:
        # a) repetitive small arrows
        xs = np.linspace(s, e, max(int((e-s)*10), 2))
        for x in xs:
            ax.annotate(
                "", xy=(x, -0.25), xytext=(x, -0.05),
                arrowprops=dict(arrowstyle="->", lw=1)
            )
        # b) shading
        ax.fill_between([s, e], -0.05, -0.2, alpha=0.3)
        # c) intensity label
        ax.text((s + e) / 2, -0.05, f"{w:.1f} kN/m", ha="center", va="bottom")

    # 5) Clean up
    ax.set_xlim(-0.05 * L, 1.05 * L)
    ax.set_ylim(-0.5 * L, 0.3 * L)
    ax.axis("off")

    return fig


def plot_sfd(beam):
    """
    Shear Force Diagram
    """
    xs = np.linspace(0, beam.length, 200)
    Vs = [beam.shear_at(x) for x in xs]
    fig, ax = plt.subplots()
    ax.plot(xs, Vs)
    ax.axhline(0, linewidth=0.5)
    ax.set_ylabel("Shear (kN)")
    ax.set_xlabel("x (m)")
    ax.set_title("Shear Force Diagram")
    return fig


def plot_bmd(beam):
    """
    Bending Moment Diagram
    """
    xs = np.linspace(0, beam.length, 200)
    Ms = [beam.moment_at(x) for x in xs]
    fig, ax = plt.subplots()
    ax.plot(xs, Ms)
    ax.axhline(0, linewidth=0.5)
    ax.set_ylabel("Moment (kN·m)")
    ax.set_xlabel("x (m)")
    ax.set_title("Bending Moment Diagram")
    return fig
