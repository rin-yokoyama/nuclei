from Nuclide import Nuclide

class DecayEvent(Nuclide):

    def __init__(self, nuclide):
        self.z = nuclide.z
        self.n = nuclide.n
        self.time = 0
        self.n_neutron = 0
