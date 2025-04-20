import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def plot_beam_diagram(beam):
    """
    Draws a schematic of the beam, supports, point loads, and UDLs.
    """
    fig, ax = plt.subplots(figsize=(8, 2))

    # Draw beam line
    ax.hlines(0, 0, beam.length, colors='black', linewidth=4)

    # Configure axes
    ax.set_xlim(-0.05 * beam.length, 1.05 * beam.length)
    ax.set_ylim(-1.0, 1.5)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.axis('off')

    # Draw supports and reaction arrows
    for i, sup in enumerate(beam.supports):
        pos = sup["pos"]
        stype = sup["type"]
        if stype == "pin":
            ax.plot(pos, 0, marker='v', color='blue', markersize=12)
        else:
            ax.plot(pos, 0, marker='o', color='green', markersize=10)
        # Annotate reaction
        if hasattr(beam, "reactions") and i < len(beam.reactions):
            R = beam.reactions[i]
            ax.annotate(
                f"{R:.2f} kN",
                xy=(pos, 0), xytext=(pos, 0.8),
                ha='center',
                arrowprops=dict(arrowstyle='->', color='magenta', lw=1.5)
            )

    # Draw point loads
    for pl in getattr(beam, "point_loads", []):
        pos = pl["pos"]
        mag = pl["mag"]
        arrow_len = 0.6
        ax.annotate(
            "",
            xy=(pos, 0), xytext=(pos, arrow_len),
            arrowprops=dict(arrowstyle='-|>', color='red', lw=2)
        )
        ax.text(pos, arrow_len + 0.1, f"{mag:.1f} kN",
                ha='center', va='bottom', color='red')

    # Draw UDLs
    for udl in getattr(beam, "distributed_loads", []):
        start, end, intensity = udl["start"], udl["end"], udl["int"]
        rect = Rectangle(
            (start, 0.3),   # (x, y)
            end - start,    # width
            0.1,            # height
            color='orange',
            alpha=0.5
        )
        ax.add_patch(rect)
        ax.text(
            (start + end) / 2,
            0.45,
            f"{intensity:.1f} kN/m",
            ha='center',
            va='bottom',
            color='orange'
        )

    return fig

def plot_sfd(beam):
    """
    Shear force diagram.
    """
    xs = np.linspace(0, beam.length, 300)
    Vs = [beam.shear_at(x) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, Vs, lw=2)
    ax.axhline(0, color='black', lw=1)
    ax.set_xlabel("Position (m)")
    ax.set_ylabel("Shear Force (kN)")
    ax.grid(True, linestyle='--', alpha=0.5)
    return fig

def plot_bmd(beam):
    """
    Bending moment diagram.
    """
    xs = np.linspace(0, beam.length, 300)
    Ms = [beam.moment_at(x) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, Ms, lw=2)
    ax.axhline(0, color='black', lw=1)
    ax.set_xlabel("Position (m)")
    ax.set_ylabel("Bending Moment (kN·m)")
    ax.grid(True, linestyle='--', alpha=0.5)
    return fig
