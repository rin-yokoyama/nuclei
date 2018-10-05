import ROOT
import yaml
import sys
from modules.NuclideGenerator import NuclideGenerator
from modules.NuclidesPlotter import NuclidesPlotter
from modules.DecaySimulator import DecaySimulator
from modules.Nuclide import NuclidePopulation
from modules.DecaySimulator import DecaySimulator
from modules.EventPlotter import EventPlotter
#from modules.PopulationPlotter import PopulationPlotter
from modules.PopulationGIFMaker import PopulationGIFMaker

if __name__ == '__main__':
    yaml_file = open(sys.argv[1],'r')
    config = yaml.load(yaml_file)
    yaml_file.close()

    nucl_gen = NuclideGenerator(config['DBFile'])
    nucl_list = nucl_gen.generateNuclides(config['DBTable'])
    print "loaded nuclear proterties of " + str(len(nucl_list)) + " nuclei from " + config['DBTable']

    init_population = []

    # initial nuclide
    n_init = NuclidePopulation()
    n_init.z = config['InitZ']
    n_init.n = config['InitN']
    n_init.counts = config['InitCounts']
    init_population.append(n_init)

    simulator = DecaySimulator(nucl_list,init_population)
    simulator.configure(config['DecaySimulator'])
    decay_list = simulator.simulateDecays()

    gif_maker = PopulationGIFMaker()
    gif_maker.configure(config['PopulationGIFMaker'])
    gif_maker.MakeGIFImage(decay_list)
    gif_maker.MakeGIF()

    rootfile = ROOT.TFile(config['OutputFile'],"recreate")
    event_plotter = EventPlotter(config['EventPlotter'])
    event_plotter.fillDecays(decay_list)
    event_plotter.writeHistograms()

    rootfile.Close() 
