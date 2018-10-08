# NuclidesPlotter.py generated by R. Yokoyama 10/04/2018
import ROOT

class NuclidesPlotter:
    # A class for plotting NuclearProperty objects as ROOT histograms
    def __init__(self, nucl_list):
        self.nucl_list = nucl_list
        self.n_range = [0,250]
        self.z_range = [0,150]

    def PlotHalfLife(self):
        # plots halflives
        hist = ROOT.TH2F("HalfLife","HalfLife",
                         self.n_range[1]-self.n_range[0], self.n_range[0]-0.5, self.n_range[1]-0.5,
                         self.n_range[1]-self.z_range[0], self.z_range[0]-0.5, self.z_range[1]-0.5)
        for nucl in self.nucl_list:
            hist.Fill(nucl.n,nucl.z,nucl.halflife)
        return hist

    def PlotPxn(self,x):
        # plots Pxn values
        hist = ROOT.TH2F("P"+str(x)+"n","P"+str(x)+"n",
                         self.n_range[1]-self.n_range[0], self.n_range[0]-0.5, self.n_range[1]-0.5,
                         self.n_range[1]-self.z_range[0], self.z_range[0]-0.5, self.z_range[1]-0.5)
        for nucl in self.nucl_list:
            hist.Fill(nucl.n,nucl.z,nucl.pn[x])
        return hist

    def SetPlotRange(self, n_range, z_range):
        # sets the plot range ( [n_low, n_up], [z_low, z_up] )
        if len(n_range) < 2 or len(z_range) < 2:
            print "[NuclidesPlotter]: invalid plot range"
            return 1
        self.n_range = n_range
        self.z_range = n_range
        return 0
