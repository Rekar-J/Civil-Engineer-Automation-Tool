import numpy as np
import matplotlib.pyplot as plt

def plot_beam_diagram(beam, load_dir="down", show_dimensions=True):
    """
    Draws:
     - beam span (thick line)
     - supports (pin=^, roller=o) pointing upward
     - point loads up or down per load_dir
     - UDL arrows + shaded region
     - optional dimension lines for overall length & per‐load location
    """
    fig, ax = plt.subplots()
    L = beam.length
    sign = -1 if load_dir == "down" else +1

    # Beam
    ax.hlines(0, 0, L, linewidth=4, color="saddlebrown")

    # Overall span dimension
    if show_dimensions:
        y_dim = 0.25 * L
        ax.annotate("", xy=(0, y_dim), xytext=(L, y_dim),
                    arrowprops=dict(arrowstyle="<->"))
        ax.text(L/2, y_dim + 0.02 * L, f"{L:.2f} m",
                ha="center", va="bottom")

    # Supports (always upward!)
    for pos, sup_type in beam.supports:
        marker = "^" if sup_type == "pin" else "o"
        ax.plot(pos, 0, marker=marker, markersize=14, color="black")

    # Point loads
    for px, pm in beam.point_loads:
        # arrow
        y0, y1 = 0.15 * sign, 0.05 * sign
        ax.annotate("", xy=(px, y1), xytext=(px, y0),
                    arrowprops=dict(arrowstyle="->", lw=2))
        ax.text(px, y0 + 0.02 * sign, f"{pm:.1f} kN",
                ha="center", va="bottom" if sign < 0 else "top")
        # per‐load dimension
        if show_dimensions:
            y_dim2 = 0.35 * L
            ax.annotate("", xy=(0, y_dim2), xytext=(px, y_dim2),
                        arrowprops=dict(arrowstyle="<->", lw=1))
            ax.text(px/2, y_dim2 + 0.01 * L, f"{px:.2f} m",
                    ha="center", va="bottom")

    # UDLs
    for s, e, w in beam.dist_loads:
        # shading
        ax.fill_between([s, e], sign * 0.05, sign * 0.15,
                        color="lightblue", alpha=0.4)
        # arrows
        xs = np.linspace(s, e, max(int((e - s) * 10), 2))
        for x in xs:
            ax.annotate("", xy=(x, sign * 0.05), xytext=(x, sign * 0.15),
                        arrowprops=dict(arrowstyle="->", lw=1))
        ax.text((s + e) / 2, sign * 0.17, f"{w:.1f} kN/m",
                ha="center", va="bottom" if sign < 0 else "top")

    ax.set_xlim(-0.05 * L, 1.05 * L)
    ax.set_ylim(-0.4 * L, 0.5 * L)
    ax.axis("off")
    return fig

def plot_sfd(beam):
    xs = np.linspace(0, beam.length, 200)
    Vs = [beam.shear_at(x) for x in xs]
    fig, ax = plt.subplots()
    ax.plot(xs, Vs, linewidth=2)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_ylabel("Shear (kN)")
    ax.set_xlabel("x (m)")
    ax.set_title("Shear Force Diagram")
    ax.grid(True, linestyle="--", alpha=0.3)
    return fig

def plot_bmd(beam):
    xs = np.linspace(0, beam.length, 200)
    Ms = [beam.moment_at(x) for x in xs]
    fig, ax = plt.subplots()
    ax.plot(xs, Ms, linewidth=2)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_ylabel("Moment (kN·m)")
    ax.set_xlabel("x (m)")
    ax.set_title("Bending Moment Diagram")
    ax.grid(True, linestyle="--", alpha=0.3)
    return fig
