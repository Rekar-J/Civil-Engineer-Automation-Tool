# core.py

import numpy as np

class Beam:
    def __init__(self, length, supports=None, loads=None):
        self.length = length
        self.supports = supports if supports is not None else []
        self.loads = loads if loads is not None else []
        self.distributed_loads = []
        self.reactions = []

    def add_support(self, pos, sup_type):
        """Register a support at position pos of type 'pin' or 'roller'."""
        self.supports.append({"pos": pos, "type": sup_type})

    def add_point_load(self, pos, mag):
        """Register a point load at position pos (kN)."""
        self.loads.append({"pos": pos, "mag": mag})

    def add_distributed_load(self, start, end, intensity):
        """Register a uniform distributed load (kN/m) from start to end."""
        self.distributed_loads.append({"start": start, "end": end, "int": intensity})

    def analyze(self):
        """Convert UDLs to equivalent point loads and compute support reactions."""
        # Convert UDLs
        for udl in self.distributed_loads:
            total = udl["int"] * (udl["end"] - udl["start"])
            x_eq = (udl["start"] + udl["end"]) / 2
            self.loads.append({"pos": x_eq, "mag": total})

        if len(self.supports) != 2:
            raise ValueError("Exactly two supports are required.")

        A, B = self.supports
        a, b = A["pos"], B["pos"]

        # ΣM about A = 0 → Rb*(b−a) = Σ[F_i*(x_i − a)]
        moment = sum(l["mag"] * (l["pos"] - a) for l in self.loads)
        Rb = moment / (b - a)
        Ra = sum(l["mag"] for l in self.loads) - Rb

        self.reactions = [Ra, Rb]

    def shear_at(self, x):
        """Shear force at position x."""
        V = 0.0
        # add reactions to left
        for idx, sup in enumerate(self.supports):
            if x >= sup["pos"]:
                V += self.reactions[idx]
        # subtract loads to left
        for l in self.loads:
            if l["pos"] <= x:
                V -= l["mag"]
        return V

    def moment_at(self, x):
        """Bending moment at position x."""
        M = 0.0
        # reactions
        for idx, sup in enumerate(self.supports):
            if x >= sup["pos"]:
                M += self.reactions[idx] * (x - sup["pos"])
        # loads
        for l in self.loads:
            if l["pos"] <= x:
                M -= l["mag"] * (x - l["pos"])
        return M
