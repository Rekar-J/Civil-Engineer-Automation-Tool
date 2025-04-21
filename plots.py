# plots.py
import numpy as np
import matplotlib.pyplot as plt

def plot_beam_diagram(beam, show_dimensions=True):
    length = beam.length
    arrow_len = length * 0.05       # shorter arrows
    fig, ax = plt.subplots()

    # Beam line
    ax.hlines(0, 0, length, colors='black', linewidth=3)

    # Supports (upward triangles)
    for pos, _ in beam.supports:
        ax.scatter(pos, 0, marker='^', s=100, color='black')

    # Point loads
    for px, pm in beam.point_loads:
        sign = np.sign(pm)
        tip_y = sign * arrow_len
        # arrow
        ax.annotate('', xy=(px, tip_y), xytext=(px, 0),
                    arrowprops=dict(arrowstyle='->', linewidth=2))
        # label
        ax.text(px, tip_y * 1.1, f"{abs(pm):.2f} kN",
                ha='center', va='bottom' if sign>0 else 'top', fontsize=8)

    # UDLs as brackets + arrows
    for s, e, w in beam.dist_loads:
        sign = np.sign(w)
        mid = (s + e)/2
        udl_arrow_len = arrow_len * 0.8
        # bracket
        bracket_y = sign * udl_arrow_len * 1.2
        ax.hlines(bracket_y, s, e, colors='gray', linestyles='dotted')
        # arrow at three points
        for x in (s, mid, e):
            ax.annotate('', xy=(x, sign*udl_arrow_len), xytext=(x,0),
                        arrowprops=dict(arrowstyle='->', linewidth=1.5, linestyle='--'))
        # intensity label
        ax.text(mid, bracket_y * 1.1, f"{abs(w):.2f} kN/m",
                ha='center', va='bottom' if sign>0 else 'top', fontsize=8)

    # Dimension lines
    if show_dimensions:
        dim_y = arrow_len * 1.3
        ax.annotate('', xy=(0, dim_y), xytext=(length, dim_y),
                    arrowprops=dict(arrowstyle='<->'))
        ax.text(length/2, dim_y*1.05, f"L = {length:.2f} m",
                ha='center', va='bottom')
        for px, _ in beam.point_loads:
            ax.vlines(px, 0, dim_y*0.05, colors='black')
            ax.text(px, dim_y*0.1, f"{px:.2f} m",
                    ha='center', va='bottom', fontsize=6)

    ax.set_xlim(-length*0.1, length*1.1)
    ax.set_ylim(-arrow_len*1.5, arrow_len*1.5)
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
