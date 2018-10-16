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

    print "opening " + config['PickledFile1'] + "..."
    input_file1 = open(config['PickledFile1'],'rb')
    decay_list1 = pickle.load(input_file1)
    input_file1.close()
    print "opened"

    print "opening " + config['PickledFile2'] + "..."
    input_file2 = open(config['PickledFile2'],'rb')
    decay_list2 = pickle.load(input_file2)
    input_file2.close()
    print "opened"

    print "making GIF animation..."
    gif_maker = PopulationGIFMaker()
    gif_maker.configure(config['PopulationGIFMaker'])
    gif_maker.MakePATHGIFImage2(decay_list1,decay_list2,config['Name1'],config['Name2'])
    gif_maker.MakeGIF()


