import time
import copy
import math
import ROOT
from DecayEvent import DecayEvent

class DecayChain(object):
    def __init__(self, initial_nucl):
        self.event_list = []
        self.initial_nuclide = initial_nucl

class DecaySimulator(object):

    def __init__(self, nucl_list, initial_population):
        self.nucl_list = nucl_list
        self.population_list = initial_population
        self.decay_chain_list = []
        self.rand = ROOT.TRandom3(int(round(time.time())))
        self.if_print = False

    def configure(self, config):
        self.if_print = bool(config['StdOutPrint'])

    def generateDecay(self, parent_nuclide, event_time):
        nucl_property = filter(lambda x: x.n == parent_nuclide.n and x.z == parent_nuclide.z, self.nucl_list)
        if not nucl_property:
            return None
        event = DecayEvent(parent_nuclide)
        t_lambda = math.log(2)/nucl_property[0].halflife 
        event.time = -1.0/t_lambda * math.log(1.0 - self.rand.Rndm()) + event_time
        for (x, pxn) in enumerate(nucl_property[0].pn):
            if self.rand.Rndm() < pxn:
                event.n_neutron = x
        if self.if_print:
            print "(N,Z): (" + str(event.n) + "," + str(event.z) + "), neutron: " + str(event.n_neutron) + ", time: " + str(event.time)
        return event

    def generateDecayChain(self, init_nuclide):
        nuclide = init_nuclide
        event_time = 0
        event_list = []
        while 1:
            event = self.generateDecay(nuclide, event_time)
            if event is None:
                break
            event_list.append(event)
            nuclide.n = nuclide.n - event.n_neutron -1
            nuclide.z = nuclide.z + 1
            event_time = event.time
        return event_list

    def simulateDecays(self):
        for nucl in self.population_list:
            for i in range(0,nucl.counts):
                if self.if_print:
                    print "DecayChain of (N,Z)=(" + str(nucl.n) + "," + str(nucl.z) + "), itr=" + str(i)
                chain = DecayChain(nucl)
                chain.event_list = self.generateDecayChain(copy.copy(nucl))
                self.decay_chain_list.append(chain)
        return self.decay_chain_list
