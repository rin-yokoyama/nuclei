import ROOT

class PopulationPlotter(object):
    def __init__(self):
        self.low_n = 0
        self.low_z = 0
        self.up_n = 250
        self.up_z = 150

    def configure(self,config):
        self.low_n = config['low_n']
        self.low_z = config['low_z']
        self.up_n = config['up_n']
        self.up_z = config['up_z']

    def plotPopulation(self, decay_chain_list, time):
        hist = ROOT.TH2I("population","population",
                         self.up_n - self.low_n, self.low_n - 0.5, self.up_n - 0.5,
                         self.up_z - self.low_z, self.low_z - 0.5, self.up_z - 0.5)
        for chain in decay_chain_list:
            nucl_after = filter(lambda x: x.time > time, chain.event_list)
            if len(nucl_after) == len(chain.event_list):
                nucleus = chain.initial_nuclide
                nucleus = nucl_after[0]
            elif len(nucl_after) == 0:
                nucleus = chain.event_list[-1]
            else:
                nucleus = nucl_after[0]
            hist.Fill(nucleus.n,nucleus.z)

        return hist
