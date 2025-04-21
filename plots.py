import numpy as np
import matplotlib.pyplot as plt

def plot_beam_diagram(beam, pl_dirs=None, udl_dirs=None, show_dimensions=True):
    """
    Draws:
     - beam span (thick line)
     - supports (pin=^, roller=o) pointing upward
     - point loads up or down per pl_dirs list
     - UDL arrows + shaded region per udl_dirs list
     - optional dimension lines for overall length & per‐load location
    """
    fig, ax = plt.subplots()
    L = beam.length

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
    for i, (px, pm) in enumerate(beam.point_loads):
        direction = pl_dirs[i] if pl_dirs and i < len(pl_dirs) else "down"
        sign = -1 if direction == "down" else 1
        # draw arrow
        y0, y1 = 0.15 * sign, 0.05 * sign
        ax.annotate("", xy=(px, y1), xytext=(px, y0),
                    arrowprops=dict(arrowstyle="->", lw=2))
        # label magnitude
        ax.text(px, y0 + 0.02 * sign, f"{abs(pm):.1f} kN",
                ha="center", va="bottom" if sign < 0 else "top")
        # per‐load dimension
        if show_dimensions:
            y_dim2 = 0.35 * L
            ax.annotate("", xy=(0, y_dim2), xytext=(px, y_dim2),
                        arrowprops=dict(arrowstyle="<->", lw=1))
            ax.text(px/2, y_dim2 + 0.01 * L, f"{px:.2f} m",
                    ha="center", va="bottom")

    # UDLs
    for i, (s, e, w) in enumerate(beam.dist_loads):
        direction = udl_dirs[i] if udl_dirs and i < len(udl_dirs) else "down"
        sign = -1 if direction == "down" else 1
        # shaded region
        ax.fill_between([s, e], sign * 0.05, sign * 0.15,
                        color="lightblue", alpha=0.4)
        # arrows along span
        xs = np.linspace(s, e, max(int((e - s) * 10), 2))
        for x in xs:
            ax.annotate("", xy=(x, sign * 0.05), xytext=(x, sign * 0.15),
                        arrowprops=dict(arrowstyle="->", lw=1))
        # label intensity
        ax.text((s + e) / 2, sign * 0.17, f"{abs(w):.1f} kN/m",
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
