# plots.py

import numpy as np
import matplotlib.pyplot as plt

def plot_sfd(beam, num=200):
    """
    Returns a matplotlib Figure showing the Shear Force Diagram for the given beam.
    
    Parameters
    ----------
    beam : Beam
        Analyzed Beam object (must have run .analyze()).
    num : int
        Number of sample points along the span.
    """
    # sample along the span
    x = np.linspace(0, beam.length, num)
    V = [beam.shear_at(xi) for xi in x]

    # create figure
    fig, ax = plt.subplots()
    ax.plot(x, V, linewidth=2)
    ax.axhline(0, color='black', linewidth=0.8)

    # mark supports
    for sup in beam.supports:
        ax.axvline(sup["pos"], linestyle='--', linewidth=1)

    ax.set_xlabel("x (m)")
    ax.set_ylabel("Shear V(x) (kN)")
    ax.set_title("Shear Force Diagram")
    ax.grid(True, which="both", linestyle=":", linewidth=0.5)
    fig.tight_layout()
    return fig

def plot_bmd(beam, num=200):
    """
    Returns a matplotlib Figure showing the Bending Moment Diagram for the given beam.
    
    Parameters
    ----------
    beam : Beam
        Analyzed Beam object (must have run .analyze()).
    num : int
        Number of sample points along the span.
    """
    x = np.linspace(0, beam.length, num)
    M = [beam.moment_at(xi) for xi in x]

    fig, ax = plt.subplots()
    ax.plot(x, M, linewidth=2)
    ax.axhline(0, color='black', linewidth=0.8)

    # mark supports
    for sup in beam.supports:
        ax.axvline(sup["pos"], linestyle='--', linewidth=1)

    ax.set_xlabel("x (m)")
    ax.set_ylabel("Moment M(x) (kN·m)")
    ax.set_title("Bending Moment Diagram")
    ax.grid(True, which="both", linestyle=":", linewidth=0.5)
    fig.tight_layout()
    return fig
