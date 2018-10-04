import time
import math
import ROOT
from DecayEvent import DecayEvent

class DecayChain(object):
    def __init__(self, initial_nucl):
        self.event_list = []
        self.initial_nuclide = initial_nucl

class DecaySimulator:

    def __init__(self, nucl_list, initial_population):
        self.nucl_list = nucl_list
        self.population_list = initial_population
        self.decay_chain_list = []
        self.rand = ROOT.TRandom3(int(round(time.time())))

    def generateDecay(self, parent_nuclide):
        nucl_property = filter(lambda x: x.n == parent_nuclide.n and x.z == parent_nuclide.z, self.nucl_list)
        if not nucl_property:
            return None
        event = DecayEvent(parent_nuclide)
        t_lambda = math.log(2)/nucl_property[0].halflife 
        event.time = -1.0/t_lambda * math.log(1.0 - self.rand.Rndm()) 
        for (x, pxn) in enumerate(nucl_property[0].pn):
            if self.rand.Rndm() < pxn:
                event.n_neutron = x
        return event

    def generateDecayChain(self, init_nuclide):
        nuclide = init_nuclide
        event_list = []
        while 1:
            event = self.generateDecay(nuclide)
            if event is None:
                break
            event_list.append(event)
            nuclide.n = nuclide.n - event.n_neutron
            nuclide.z = nuclide.z - 1
        return event_list

    def simulateDecays(self):
        for nucl in self.population_list:
            for i in range(nucl.counts):
                chain = DecayChain(nucl)
                chain.event_list = self.generateDecayChain(nucl)
                self.decay_chain_list.append(chain)
        return self.decay_chain_list
