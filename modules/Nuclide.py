class Nuclide(object):
    def __init__(self):
        self.z = 0
        self.n = 0

class NuclideProperty(Nuclide):
    def __init__(self):
        self.pn = []
        self.halflife = 0.

class NuclidePopulation(Nuclide):
    def __init__(self):
        self.counts = 0
