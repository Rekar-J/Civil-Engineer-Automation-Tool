# core.py

class Beam:
    def __init__(self, length, supports=None, loads=None):
        """
        length : float
            Span of the beam (m).
        supports : list of dict, optional
            Pre‐defined supports, each as {"pos": x, "type": "pin"/"roller"}.
        loads : list of dict, optional
            Pre‐defined point loads, each as {"pos": x, "mag": kN}.
        """
        self.length = length
        self.supports = []
        self.point_loads = []
        self.udls = []  # uniform distributed loads
        self.reactions = []

        # If user passed initial supports/loads, register them
        if supports:
            for sup in supports:
                self.add_support(sup["pos"], sup["type"])
        if loads:
            for pl in loads:
                self.add_point_load(pl["pos"], pl["mag"])

    def add_support(self, pos, sup_type="pin"):
        """Register a support at position pos (m)."""
        if len(self.supports) >= 2:
            raise ValueError("Only up to two supports are allowed.")
        if not (0 <= pos <= self.length):
            raise ValueError("Support position must be within [0, L].")
        self.supports.append({"pos": pos, "type": sup_type})

    def add_point_load(self, pos, mag):
        """Register a downward point‐load of magnitude mag (kN) at pos (m)."""
        if not (0 <= pos <= self.length):
            raise ValueError("Load position must be within [0, L].")
        self.point_loads.append({"pos": pos, "mag": mag})

    def add_distributed_load(self, start, end, intensity):
        """
        Register a uniform distributed load of intensity (kN/m)
        acting from x=start to x=end.
        """
        if not (0 <= start < end <= self.length):
            raise ValueError("UDL start/end must satisfy 0 ≤ start < end ≤ L.")
        self.udls.append({"start": start, "end": end, "int": intensity})

    def analyze(self):
        """
        Compute reactions at the two supports by static equilibrium.
        Must have exactly 2 supports registered.
        """
        if len(self.supports) != 2:
            raise ValueError("Analysis requires exactly two supports.")

        # Equivalent point‐loads for UDLs
        equiv = []
        for pl in self.point_loads:
            equiv.append({"P": pl["mag"], "a": pl["pos"]})
        for ud in self.udls:
            w = ud["int"] * (ud["end"] - ud["start"])
            a = (ud["start"] + ud["end"]) / 2
            equiv.append({"P": w, "a": a})

        # Total downward load
        total_load = sum(item["P"] for item in equiv)

        # Support positions
        A, B = self.supports[0]["pos"], self.supports[1]["pos"]
        Lspan = B - A
        if Lspan <= 0:
            raise ValueError("Second support must lie to the right of the first.")

        # Sum of moments about B = RA * span
        M_about_B = sum(item["P"] * (B - item["a"]) for item in equiv)
        RA = M_about_B / Lspan
        RB = total_load - RA

        self.reactions = [RA, RB]
        return self.reactions

    def shear_at(self, x):
        """
        Shear force V(x): 
        +Reactions to the left minus loads to the left of x.
        """
        V = 0.0

        # Add reactions
        for i, sup in enumerate(self.supports):
            if sup["pos"] <= x:
                V += self.reactions[i]

        # Subtract point loads
        for pl in self.point_loads:
            if pl["pos"] <= x:
                V -= pl["mag"]

        # Subtract UDL contributions
        for ud in self.udls:
            if ud["start"] < x:
                length = min(x, ud["end"]) - ud["start"]
                if length > 0:
                    V -= ud["int"] * length

        return V

    def moment_at(self, x):
        """
        Bending moment M(x):
        Integrate shear, or sum moments of each force about x.
        """
        M = 0.0

        # Contribution from reactions
        for i, sup in enumerate(self.supports):
            if sup["pos"] <= x:
                M += self.reactions[i] * (x - sup["pos"])

        # Contribution from point loads
        for pl in self.point_loads:
            if pl["pos"] <= x:
                M -= pl["mag"] * (x - pl["pos"])

        # Contribution from UDLs
        for ud in self.udls:
            if ud["start"] < x:
                length = min(x, ud["end"]) - ud["start"]
                if length > 0:
                    w_eq = ud["int"] * length
                    a_bar = ud["start"] + length / 2
                    M -= w_eq * (x - a_bar)

        return M
