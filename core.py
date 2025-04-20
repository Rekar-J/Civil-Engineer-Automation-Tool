import numpy as np

class Beam:
    def __init__(self, length, supports=None, loads=None):
        self.length = length
        self.supports = []
        self.point_loads = []
        self.dist_loads = []
        self.reactions = []
        self._point_loads = []
        if supports:
            for s in supports:
                self.add_support(*s)
        if loads:
            for l in loads:
                if "mag" in l:
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
        # Convert UDL → eq. point loads
        eq = []
        for s,e,w in self.dist_loads:
            L = e - s
            eq.append((s + L/2, w * L))
        loads = self.point_loads + eq

        if len(self.supports) != 2:
            raise ValueError("Need exactly 2 supports.")
        a, _ = self.supports[0]
        b, _ = self.supports[1]

        # reactions for simply supported
        M_A = sum(m * (x - a) for x,m in loads)
        W   = sum(m for _,m in loads)
        Rb  = M_A / (b - a)
        Ra  = W - Rb
        self.reactions = [Ra, Rb]
        self._point_loads = loads

    def shear_at(self, x):
        V = 0.0
        if self.reactions and x >= self.supports[0][0]:
            V += self.reactions[0]
        for px, pm in self._point_loads:
            if px <= x:
                V -= pm
        return V

    def moment_at(self, x):
        M = 0.0
        if self.reactions and x >= self.supports[0][0]:
            M += self.reactions[0] * (x - self.supports[0][0])
        for px, pm in self._point_loads:
            if px <= x:
                M -= pm * (x - px)
        return M
