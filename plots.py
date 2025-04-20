# plots.py

import numpy as np
import matplotlib.pyplot as plt

def plot_sfd(beam):
    """Return a Matplotlib Figure for the shear force diagram."""
    xs = np.linspace(0, beam.length, 300)
    Vs = [beam.shear_at(x) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, Vs, linewidth=2)
    ax.axhline(0, linestyle="--")
    ax.set_title("Shear Force Diagram")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("V (kN)")
    ax.grid(True)
    return fig

def plot_bmd(beam):
    """Return a Matplotlib Figure for the bending moment diagram."""
    xs = np.linspace(0, beam.length, 300)
    Ms = [beam.moment_at(x) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, Ms, linewidth=2)
    ax.axhline(0, linestyle="--")
    ax.set_title("Bending Moment Diagram")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("M (kN·m)")
    ax.grid(True)
    return fig
