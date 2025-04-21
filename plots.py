# plots.py
import numpy as np
import matplotlib.pyplot as plt

def plot_beam_diagram(beam, show_dimensions=True):
    length = beam.length
    arrow_len = length * 0.1
    fig, ax = plt.subplots()

    # Beam line
    ax.hlines(0, 0, length, colors='black', linewidth=3)

    # Supports (upward triangles)
    for pos, _ in beam.supports:
        ax.scatter(pos, 0, marker='^', s=100, color='black')

    # Point loads
    for px, pm in beam.point_loads:
        sign = 1 if pm > 0 else -1
        ax.annotate(
            '',
            xy=(px, sign * arrow_len),
            xytext=(px, 0),
            arrowprops=dict(arrowstyle='->', linewidth=2)
        )

    # UDLs as multiple arrows + bracket
    for s, e, w in beam.dist_loads:
        sign = 1 if w > 0 else -1
        mid = (s + e) / 2
        udl_arrow_len = arrow_len * 0.8
        for x in (s, mid, e):
            ax.annotate(
                '',
                xy=(x, sign * udl_arrow_len),
                xytext=(x, 0),
                arrowprops=dict(arrowstyle='->', linewidth=1.5, linestyle='--')
            )
        bracket_y = sign * udl_arrow_len * 1.2
        ax.hlines(bracket_y, s, e, colors='gray', linestyles='dotted')

    # Dimension lines
    if show_dimensions:
        dim_y = arrow_len * 1.3
        # total span
        ax.annotate(
            '',
            xy=(0, dim_y),
            xytext=(length, dim_y),
            arrowprops=dict(arrowstyle='<->')
        )
        ax.text(length / 2, dim_y * 1.05, f"L = {length:.2f} m",
                ha='center', va='bottom')
        # load positions ticks
        for px, _ in beam.point_loads:
            ax.plot([px, px], [0, dim_y * 0.05], color='black')
            ax.text(px, dim_y * 0.1, f"{px:.2f} m",
                    ha='center', va='bottom', fontsize=8)

    # Tidy up
    ax.set_xlim(-length * 0.1, length * 1.1)
    ax.set_ylim(-arrow_len * 1.5, arrow_len * 1.5)
    ax.axis('off')
    return fig


def plot_sfd(beam):
    xs = np.linspace(0, beam.length, 200)
    Vs = [beam.shear_at(x) for x in xs]
    fig, ax = plt.subplots()
    ax.plot(xs, Vs)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_ylabel("Shear (kN)")
    ax.set_xlabel("x (m)")
    ax.set_title("Shear Force Diagram")
    return fig


def plot_bmd(beam):
    xs = np.linspace(0, beam.length, 200)
    Ms = [beam.moment_at(x) for x in xs]
    fig, ax = plt.subplots()
    ax.plot(xs, Ms)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_ylabel("Moment (kN·m)")
    ax.set_xlabel("x (m)")
    ax.set_title("Bending Moment Diagram")
    return fig
