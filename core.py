import numpy as np

class Support:
    def __init__(self, position, kind='pin'):
        self.position = position
        self.kind = kind  # 'pin', 'roller', 'fixed'
        self.reaction = 0.0

class PointLoad:
    def __init__(self, magnitude, position):
        self.magnitude = magnitude
        self.position = position

class DistributedLoad:
    def __init__(self, magnitude, start, end):
        self.magnitude = magnitude  # uniform load (kN/m)
        self.start = start
        self.end = end

    def equivalent_point_load(self):
        length = self.end - self.start
        return PointLoad(
            magnitude=self.magnitude * length,
            position=(self.start + self.end) / 2
        )

class Beam:
    def __init__(self, length):
        self.length = length
        self.supports = []
        self.point_loads = []
        self.distributed_loads = []

    def add_support(self, position, kind='pin'):
        self.supports.append(Support(position, kind))

    def add_point_load(self, magnitude, position):
        self.point_loads.append(PointLoad(magnitude, position))

    def add_distributed_load(self, magnitude, start, end):
        self.distributed_loads.append(DistributedLoad(magnitude, start, end))

    def compute_reactions(self):
        """
        Currently supports two supports (simply supported beam).
        For fixed supports or indeterminate systems, symbolic methods are needed.
        """
        if len(self.supports) != 2:
            raise NotImplementedError("Only simply supported beams with 2 supports are supported.")

        a = self.supports[0].position
        b = self.supports[1].position
        L = b - a

        # Combine point loads and equivalent point loads from distributed loads
        all_loads = self.point_loads[:]
        for dload in self.distributed_loads:
            all_loads.append(dload.equivalent_point_load())

        total_moment_b = sum([load.magnitude * (load.position - b) for load in all_loads])
        reaction_a = total_moment_b / L
        total_load = sum([load.magnitude for load in all_loads])
        reaction_b = total_load - reaction_a

        self.supports[0].reaction = reaction_a
        self.supports[1].reaction = reaction_b

        return reaction_a, reaction_b

    def shear_force(self, x):
        V = 0.0

        for support in self.supports:
            if x >= support.position:
                V += support.reaction

        for load in self.point_loads:
            if x >= load.position:
                V -= load.magnitude

        for dload in self.distributed_loads:
            if x >= dload.start:
                length = min(x, dload.end) - dload.start
                if length > 0:
                    V -= dload.magnitude * length

        return V

    def bending_moment(self, x):
        M = 0.0

        for support in self.supports:
            if x >= support.position:
                M += support.reaction * (x - support.position)

        for load in self.point_loads:
            if x >= load.position:
                M -= load.magnitude * (x - load.position)

        for dload in self.distributed_loads:
            if x >= dload.start:
                length = min(x, dload.end) - dload.start
                if length > 0:
                    a = dload.start
                    w = dload.magnitude
                    M -= w * length * (x - a - length / 2)

        return M

    def analyze(self, resolution=100):
        self.compute_reactions()
        x_vals = np.linspace(0, self.length, resolution)
        V = np.array([self.shear_force(x) for x in x_vals])
        M = np.array([self.bending_moment(x) for x in x_vals])
        return x_vals, V, M
