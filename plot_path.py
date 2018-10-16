import ROOT
import sys
import yaml
import pickle
import bz2
from modules.EventPlotter import EventPlotter
from modules.PopulationGIFMaker import PopulationGIFMaker

if __name__ == '__main__':
    yaml_file = open(sys.argv[1],'r')
    config = yaml.load(yaml_file)
    yaml_file.close()

    print "opening " + config['PickledFile'] + "..."
    #input_file = bz2.BZ2File(config['PickledFile'],'rb')
    input_file = open(config['PickledFile'],'rb')
    decay_list = pickle.load(input_file)
    input_file.close()
    print "opened"

    print "making GIF animation..."
    gif_maker = PopulationGIFMaker()
    gif_maker.configure(config['PopulationGIFMaker'])
    gif_maker.MakePATHGIFImage(decay_list)
    gif_maker.MakeGIF()


