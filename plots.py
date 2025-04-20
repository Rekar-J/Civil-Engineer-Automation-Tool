import numpy as np
import matplotlib.pyplot as plt

def plot_sfd(beam):
    xs = np.linspace(0, beam.length, 200)
    Vs = [beam.shear_at(x) for x in xs]
    fig, ax = plt.subplots()
    ax.plot(xs, Vs)
    ax.axhline(0, linewidth=0.5)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Shear (kN)")
    return fig

def plot_bmd(beam):
    xs = np.linspace(0, beam.length, 200)
    Ms = [beam.moment_at(x) for x in xs]
    fig, ax = plt.subplots()
    ax.plot(xs, Ms)
    ax.axhline(0, linewidth=0.5)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Moment (kN·m)")
    return fig
