# plots.py

import numpy as np
import matplotlib.pyplot as plt

def plot_beam_diagram(beam):
    """
    Draws a simple schematic of the beam with supports and point loads.
    """
    fig, ax = plt.subplots(figsize=(6, 2))
    # Draw the beam as a horizontal line
    ax.hlines(0, 0, beam.length, colors='black', linewidth=3)
    
    # Plot supports
    for pos, sup_type in beam.supports:
        if sup_type == "pin":
            # Triangular support
            triangle = plt.Polygon(
                [[pos - 0.1, -0.2], [pos + 0.1, -0.2], [pos, 0]],
                closed=True, edgecolor="black", facecolor="none", linewidth=2
            )
            ax.add_patch(triangle)
        else:  # roller
            # Roller as a circle under the beam
            circle = plt.Circle((pos, -0.1), 0.07, edgecolor="black", facecolor="none", linewidth=2)
            ax.add_patch(circle)
    
    # Plot point loads
    for x, m in beam.point_loads:
        ax.annotate(
            "", xy=(x, 0.5), xytext=(x, 0.1),
            arrowprops=dict(arrowstyle="->", linewidth=2)
        )
        ax.text(x, 0.55, f"{m:.1f} kN", ha="center", va="bottom")
    
    ax.set_xlim(-0.1 * beam.length, 1.1 * beam.length)
    ax.set_ylim(-0.5, 1)
    ax.axis("off")
    ax.set_title("Beam Schematic", pad=10)
    return fig

def plot_sfd(beam):
    """
    Shear Force Diagram
    """
    xs = np.linspace(0, beam.length, 200)
    Vs = [beam.shear_at(x) for x in xs]
    fig, ax = plt.subplots()
    ax.plot(xs, Vs)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_ylabel("Shear (kN)")
    ax.set_xlabel("x (m)")
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
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_ylabel("Moment (kN·m)")
    ax.set_xlabel("x (m)")
    ax.set_title("Bending Moment Diagram")
    return fig
