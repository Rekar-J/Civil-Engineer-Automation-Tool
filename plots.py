import matplotlib.pyplot as plt
import numpy as np

def plot_beam_diagram(beam):
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.hlines(0, 0, beam.length, colors='black', linewidth=2)

    # Supports
    for support in beam.supports:
        if support.kind == 'pin':
            ax.plot(support.position, 0, 'v', color='blue', markersize=12, label='Pin support')
        elif support.kind == 'roller':
            ax.plot(support.position, 0, 'v', color='green', markersize=12, label='Roller support')
        elif support.kind == 'fixed':
            ax.plot(support.position, 0, '^', color='purple', markersize=12, label='Fixed support')

    # Point loads
    for load in beam.point_loads:
        ax.arrow(load.position, 0.5, 0, -0.4, head_width=0.1, head_length=0.1, fc='red', ec='red')
        ax.text(load.position, 0.6, f'{load.magnitude} kN', ha='center', color='red')

    # Distributed loads
    for dload in beam.distributed_loads:
        xs = np.linspace(dload.start, dload.end, 20)
        for x in xs:
            ax.arrow(x, 0.4, 0, -0.3, head_width=0.05, head_length=0.05, fc='orange', ec='orange')
        ax.text((dload.start + dload.end) / 2, 0.5, f'{dload.magnitude} kN/m', ha='center', color='orange')

    ax.set_xlim(-0.5, beam.length + 0.5)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    ax.set_title("Beam Diagram")
    plt.tight_layout()
    return fig

def plot_sfd(x, V):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(x, V, label='Shear Force', color='blue')
    ax.fill_between(x, V, 0, alpha=0.3)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_title("Shear Force Diagram (SFD)")
    ax.set_xlabel("Length (m)")
    ax.set_ylabel("Shear Force (kN)")
    ax.grid(True)
    plt.tight_layout()
    return fig

def plot_bmd(x, M):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(x, M, label='Bending Moment', color='green')
    ax.fill_between(x, M, 0, alpha=0.3)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_title("Bending Moment Diagram (BMD)")
    ax.set_xlabel("Length (m)")
    ax.set_ylabel("Moment (kNm)")
    ax.grid(True)
    plt.tight_layout()
    return fig
