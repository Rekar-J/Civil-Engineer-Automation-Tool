import numpy as np

class Beam:
    def __init__(self, length, supports=None, loads=None):
        """
        length: span of the beam (m)
        supports: list of {"pos": x, "type": "pin"|"roller"} (optional)
        loads: list of {"pos": x, "mag": P} for point loads (optional)
        """
        self.length = length
        self.supports = []
        self.point_loads = []
        self.distributed_loads = []
        self.reactions = []

        if supports:
            for sup in supports:
                self.add_support(sup["pos"], sup["type"])
        if loads:
            for pl in loads:
                self.add_point_load(pl["pos"], pl["mag"])

    def add_support(self, pos, sup_type):
        if sup_type not in ("pin", "roller"):
            raise ValueError("Support type must be 'pin' or 'roller'")
        self.supports.append({"pos": pos, "type": sup_type})

    def add_point_load(self, pos, mag):
        self.point_loads.append({"pos": pos, "mag": mag})

    def add_distributed_load(self, start, end, intensity):
        if end < start:
            raise ValueError("UDL end must be ≥ start")
        self.distributed_loads.append({"start": start, "end": end, "int": intensity})

    def analyze(self):
        """
        Compute support reactions for a simply-supported beam with two supports.
        Distributed loads are converted to equivalent point loads.
        """
        # 1) build list of equivalent point loads
        eq_loads = []
        eq_loads += [{"pos": pl["pos"], "mag": pl["mag"]} for pl in self.point_loads]
        for udl in self.distributed_loads:
            w = udl["int"] * (udl["end"] - udl["start"])
            x = 0.5 * (udl["start"] + udl["end"])
            eq_loads.append({"pos": x, "mag": w})

        # 2) total load
        W = sum(l["mag"] for l in eq_loads)

        # 3) must have exactly two supports
        if len(self.supports) != 2:
            raise ValueError("Beam must have exactly 2 supports to analyze")
        # sort supports by position
        self.supports.sort(key=lambda s: s["pos"])
        x1 = self.supports[0]["pos"]
        x2 = self.supports[1]["pos"]

        # 4) take moments about support1 to find R2
        M_about_1 = sum(l["mag"] * (l["pos"] - x1) for l in eq_loads)
        R2 = M_about_1 / (x2 - x1)
        R1 = W - R2

        self.reactions = [R1, R2]

    def shear_at(self, x):
        """
        V(x) = sum(reactions at supports ≤ x) 
               − sum(point loads at pos ≤ x)
               − sum(UDL contribution up to x)
        """
        V = 0.0
        # reactions
        for R, sup in zip(self.reactions, self.supports):
            if x >= sup["pos"]:
                V += R
        # point loads
        for pl in self.point_loads:
            if x >= pl["pos"]:
                V -= pl["mag"]
        # distributed loads
        for udl in self.distributed_loads:
            if x <= udl["start"]:
                continue
            elif udl["start"] < x < udl["end"]:
                V -= udl["int"] * (x - udl["start"])
            else:
                V -= udl["int"] * (udl["end"] - udl["start"])
        return V

    def moment_at(self, x):
        """
        M(x) = ∫₀ˣ V(s) ds  (numerical integration)
        """
        xs = np.linspace(0, x, 200)
        Vs = [self.shear_at(s) for s in xs]
        return np.trapz(Vs, xs)
