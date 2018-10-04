import ROOT
from modules.NuclideGenerator import NuclideGenerator
from modules.NuclidesPlotter import NuclidesPlotter
from modules.DecaySimulator import DecaySimulator
from modules.Nuclide import NuclidePopulation

if __name__ == '__main__':
    nucl_gen = NuclideGenerator("db/nuclei.db")
    nucl_list = nucl_gen.generateNuclides("frdm_beoh")
    print len(nucl_list)
    plotter = NuclidesPlotter(nucl_list)
    plotter.SetPlotRange([40,100],[20,40])
    hist1 = plotter.PlotHalfLife() 
    hist2 = plotter.PlotPxn(1) 

    init_population = []
    ga86 = NuclidePopulation()
    ga86.z = 31
    ga86.n = 55
    ga86.counts = 100
    init_population.append(ga86)
    simulator = DecaySimulator(nucl_list,init_population)
    decay_list = simulator.simulateDecays()
    print decay_list
    hist3 = ROOT.TH1F("n_decay","n_decay",100,0,100)
    for decay in decay_list:
        hist3.Fill(len(decay.event_list))

    rootfile = ROOT.TFile("test.root","recreate")
    hist1.Write()
    hist2.Write()
    hist3.Write()
    rootfile.Close() 
