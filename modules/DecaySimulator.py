# DecaySimulator.py generated by R. Yokoyama on 10/05/2018
import time
import copy
import math
import ROOT
from DecayEvent import DecayEvent

class DecayChain(object):
    # a container of a decay chain event
    def __init__(self, initial_nucl):
        self.event_list = []
        self.initial_nuclide = initial_nucl

class DecaySimulator(object):
    # A class to make Monte Carlo simulation of beta decays.
    def __init__(self, nucl_list, initial_population):
        self.nucl_list = nucl_list
        self.population_list = initial_population 
        self.decay_chain_list = []
        self.rand = ROOT.TRandom3(int(round(time.time())))
        self.if_print = False

    def configure(self, config):
        # configures by a given yaml node
        self.if_print = bool(config['StdOutPrint']) # if this is ture, it prints every decay events as text

    def generateDecay(self, parent_nuclide, event_time):
        # simulates one decay event and returns a DecayEvent object
        nucl_property = filter(lambda x: x.n == parent_nuclide.n and x.z == parent_nuclide.z, self.nucl_list)
        if not nucl_property: # returns None if there is no decay property for the nuclide in the database
            return None
        event = DecayEvent(parent_nuclide)
        t_lambda = math.log(2)/nucl_property[0].halflife
        event.time = -1.0/t_lambda * math.log(1.0 - self.rand.Rndm()) + event_time  # exponential random number
        sum_pxn = 0
        rand = self.rand.Rndm()
        for (x, pxn) in enumerate(nucl_property[0].pn): # choses number of neutron to emit from the random number
            sum_pxn = sum_pxn + pxn
            if rand > sum_pxn:
                event.n_neutron = x+1

        if self.if_print: # prints the decay event if StdOutPrint is ture
            print "(N,Z): (" + str(event.n) + "," + str(event.z) + "), neutron: " + str(event.n_neutron) + ", time: " + str(event.time)
        return event

    def generateDecayChain(self, init_nuclide):
        # generates a decay chain and returns a DecayChain object
        nuclide = init_nuclide
        event_time = 0
        event_list = []
        while 1: # loops until it ends up in a stable nuclide
            event = self.generateDecay(nuclide, event_time)
            if event is None:
                break
            event_list.append(event)
            nuclide.n = nuclide.n - event.n_neutron -1
            nuclide.z = nuclide.z + 1
            event_time = event.time
        return event_list

    def simulateDecays(self):
        # simulate decays for all the initial populations and returns a lost of DecayChain objects
        for nucl in self.population_list:
            for i in range(0,nucl.counts):
                if self.if_print:
                    print "DecayChain of (N,Z)=(" + str(nucl.n) + "," + str(nucl.z) + "), itr=" + str(i)
                chain = DecayChain(nucl)
                chain.event_list = self.generateDecayChain(copy.copy(nucl))
                self.decay_chain_list.append(chain)
        return self.decay_chain_list
