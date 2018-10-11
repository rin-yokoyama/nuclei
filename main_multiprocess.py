import ROOT
import yaml
import sys
import multiprocessing
import bz2
import pickle
from modules.NuclideGenerator import NuclideGenerator
from modules.NuclidesPlotter import NuclidesPlotter
from modules.DecaySimulator import DecaySimulator
from modules.Nuclide import NuclidePopulation
from modules.DecaySimulator import DecaySimulator
from modules.EventPlotter import EventPlotter
from modules.PopulationGIFMaker import PopulationGIFMaker

def worker(simulator, queue):
    queue.put(simulator.simulateDecays())

if __name__ == '__main__':
    # opens yaml config file
    yaml_file = open(sys.argv[1],'r')
    config = yaml.load(yaml_file)
    yaml_file.close()

    # generates a list of NuclideProperty objects from the DB
    nucl_gen = NuclideGenerator(config['DBFile'])
    nucl_list = nucl_gen.generateNuclides(config['DBTable'])
    print "loaded nuclear proterties of " + str(len(nucl_list)) + " nuclei from " + config['DBTable']

    init_population = []

    n_workers = config['NWorkers']
    # generate a list of initial nuclides
    n_total = 0
    for nucl in config['InitialNuclides']:
        n_init = NuclidePopulation()
        n_init.z = nucl['InitZ']
        n_init.n = nucl['InitN']
        n_init.counts = int( nucl['InitCounts'] / n_workers )
        init_population.append(n_init)
        n_total = n_total + n_init.counts

    print "total number of trial = " + str(n_total) + " * " + str(n_workers) + " (processes)"

    # starts parallel jobs
    queues = []
    for i in range(0,n_workers):
        simulator = DecaySimulator(nucl_list,init_population)
        simulator.configure(config['DecaySimulator'])
        q = multiprocessing.Queue()
        job = multiprocessing.Process( target = worker, args = (simulator, q, ) )
        queues.append(q)
        job.start()
        print "started process #" + str(i)

    # waits for all the jobs to be done.
    decay_list = []
    print "waiting for all the queues to be filled..."
    for (i,queue) in enumerate(queues):
        decay_list.extend(queue.get())
        print "recieved queue #" + str(i)

    # writes decay_list to a file using pickle module
    #output_file = bz2.BZ2File(config['PickledFile'],'w')
    output_file = open(config['PickledFile'],'w')
    print "writing decay_list to " + config['PickledFile'] + "..."
    pickle.dump(decay_list, output_file)
    output_file.close()

    print "done"

