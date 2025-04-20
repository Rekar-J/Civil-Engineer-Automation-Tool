# core.py

from dataclasses import dataclass
from typing import List


@dataclass
class Support:
    position: float
    type: str  # 'fixed', 'pinned', or 'roller'


@dataclass
class Load:
    magnitude: float
    position: float
    type: str  # 'point', 'udl', or 'moment'


@dataclass
class Beam:
    length: float
    supports: List[Support]
    loads: List[Load]

    def calculate_reactions(self):
        """
        Very basic reaction calculator:
        - Handles statically determinate beams with two supports and point loads only.
        - Only works for simply supported beam with pinned and roller.
        """
        if len(self.supports) != 2:
            raise ValueError("Only two-support systems are supported in this version.")

        a = self.supports[0].position
        b = self.supports[1].position
        L = b - a
        total_load = sum(load.magnitude for load in self.loads if load.type == 'point')
        moments = sum(load.magnitude * (load.position - a) for load in self.loads if load.type == 'point')

        R2 = moments / L
        R1 = total_load - R2

        return {
            f"R@{a}": R1,
            f"R@{b}": R2
        }

    def shear_force_diagram(self, step=0.1):
        """
        Returns list of tuples (x, shear) at each step.
        Simplified for point loads only.
        """
        reactions = self.calculate_reactions()
        shear_values = []
        current_shear = 0

        x = 0
        while x <= self.length:
            current_shear = 0
            for key, reaction in reactions.items():
                pos = float(key.split('@')[1])
                if x >= pos:
                    current_shear += reaction

            for load in self.loads:
                if load.type == 'point' and x >= load.position:
                    current_shear -= load.magnitude

            shear_values.append((x, current_shear))
            x += step

        return shear_values

    def bending_moment_diagram(self, step=0.1):
        """
        Returns list of tuples (x, moment) at each step.
        Simplified for point loads only.
        """
        reactions = self.calculate_reactions()
        moment_values = []

        x = 0
        while x <= self.length:
            moment = 0
            for key, reaction in reactions.items():
                pos = float(key.split('@')[1])
                if x >= pos:
                    moment += reaction * (x - pos)

            for load in self.loads:
                if load.type == 'point' and x >= load.position:
                    moment -= load.magnitude * (x - load.position)

            moment_values.append((x, moment))
            x += step

        return moment_values
