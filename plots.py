import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

@st.cache_data
def plot_sfd(beam, num_points: int = 500):
    """
    Shear Force Diagram (SFD)
    """
    # sample positions along the beam
    xs = np.linspace(0, beam.length, num_points)
    # compute shear at each x
    shear = [beam.shear_at(x) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, shear, linewidth=2)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_title("Shear Force Diagram")
    ax.set_xlabel("Position (m)")
    ax.set_ylabel("Shear Force (kN)")
    ax.grid(True)
    return fig

@st.cache_data
def plot_bmd(beam, num_points: int = 500):
    """
    Bending Moment Diagram (BMD)
    """
    xs = np.linspace(0, beam.length, num_points)
    moment = [beam.moment_at(x) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, moment, linewidth=2)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_title("Bending Moment Diagram")
    ax.set_xlabel("Position (m)")
    ax.set_ylabel("Bending Moment (kN·m)")
    ax.grid(True)
    return fig
