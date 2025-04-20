import numpy as np

class Beam:
    def __init__(self, length, supports=None, loads=None):
        self.length = length
        self.supports = supports or []      # each: (position, type)
        self.point_loads = []               # each: (pos, mag)
        self.dist_loads = []                # each: (start, end, intensity)
        self.reactions = []
        if supports:
            for s in supports:
                self.add_support(*s)
        if loads:
            for l in loads:
                if l.get("mag") is not None:
                    self.add_point_load(l["pos"], l["mag"])
                else:
                    self.add_distributed_load(l["start"], l["end"], l["intensity"])

    def add_support(self, pos, sup_type="pin"):
        self.supports.append((pos, sup_type))

    def add_point_load(self, pos, mag):
        self.point_loads.append((pos, mag))

    def add_distributed_load(self, start, end, intensity):
        self.dist_loads.append((start, end, intensity))

    def analyze(self):
        # Convert dist. loads to equivalent point loads
        eq_loads = []
        for s, e, w in self.dist_loads:
            L = e - s
            eq_loads.append((s + L/2, w * L))
        total_loads = self.point_loads + eq_loads

        # Reaction calc for simply supported two‑point beam
        if len(self.supports) != 2:
            raise ValueError("Need exactly 2 supports to solve.")
        a, _ = self.supports[0]
        b, _ = self.supports[1]
        L = self.length
        # sum of moments about A and sum loads
        M_A = sum(m * (x - a) for x, m in total_loads)
        W   = sum(m for _, m in total_loads)
        Rb  = M_A / (b - a)
        Ra  = W - Rb
        self.reactions = [Ra, Rb]

        # Build internal arrays for f(x) and M(x)
        self._point_loads = total_loads

    def shear_at(self, x):
        V = 0.0
        # left reaction
        if self.reactions and x >= self.supports[0][0]:
            V += self.reactions[0]
        # minus any point loads to left of x
        for px, pm in self._point_loads:
            if px <= x:
                V -= pm
        return V

    def moment_at(self, x):
        M = 0.0
        # left reaction moment
        if self.reactions and x >= self.supports[0][0]:
            M += self.reactions[0] * (x - self.supports[0][0])
        # minus moments from loads left of x
        for px, pm in self._point_loads:
            if px <= x:
                M -= pm * (x - px)
        return M
