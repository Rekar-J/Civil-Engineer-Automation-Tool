# plots.py

import numpy as np
import matplotlib.pyplot as plt

def plot_beam_diagram(beam, load_dir="down", show_dimensions=True):
    fig, ax = plt.subplots()
    L = beam.length
    sign = -1 if load_dir=="down" else +1

    # Beam line
    ax.hlines(0, 0, L, linewidth=4)

    # --- Dimensions ---
    if show_dimensions:
        y_len = 0.25 * L
        ax.annotate(
            "",
            xy=(0, y_len), xytext=(L, y_len),
            arrowprops=dict(arrowstyle="<->")
        )
        ax.text(L/2, y_len + 0.02 * L, f"{L:.2f} m", ha="center", va="bottom")

    # Supports (upward!)
    for pos, sup_type in beam.supports:
        marker = "^" if sup_type=="pin" else "o"
        ax.plot(pos, 0, marker=marker, markersize=12)

    # Point loads
    for px, pm in beam.point_loads:
        y_start = 0.1 * sign
        y_end   = (0.05 * sign)
        ax.annotate(
            "",
            xy=(px, y_end),
            xytext=(px, y_start),
            arrowprops=dict(arrowstyle="->", lw=2)
        )
        ax.text(px, y_end + 0.02*sign, f"{pm:.1f} kN", ha="center", va="bottom" if sign<0 else "top")
        # Per‐load dimension
        if show_dimensions:
            y_pl = 0.15 * L
            ax.annotate(
                "",
                xy=(0, y_pl), xytext=(px, y_pl),
                arrowprops=dict(arrowstyle="<->", lw=1)
            )
            ax.text(px/2, y_pl + 0.01*L, f"{px:.2f} m", ha="center", va="bottom")

    # UDLs
    for s, e, w in beam.dist_loads:
        # Arrows
        xs = np.linspace(s, e, max(int((e-s)*10), 2))
        for x in xs:
            ax.annotate(
                "",
                xy=(x, sign*0.05), xytext=(x, sign*0.15),
                arrowprops=dict(arrowstyle="->", lw=1)
            )
        # Shading
        ax.fill_between([s, e], sign*0.05, sign*0.15, alpha=0.3)
        ax.text((s+e)/2, sign*0.17, f"{w:.1f} kN/m", ha="center", va="bottom")

    ax.set_xlim(-0.05*L, 1.05*L)
    ax.set_ylim(-0.3*L, 0.4*L)
    ax.axis("off")
    return fig

# … plot_sfd and plot_bmd unchanged …
