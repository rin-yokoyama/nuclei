from PopulationPlotter import PopulationPlotter
from ROOT import gStyle
from ROOT import gPad
import os

class PopulationGIFMaker(object):
    def __init__(self):
        self.plotter = PopulationPlotter()
        self.time_list = []

    def configure(self, config):
        self.plotter.configure(config['PopulationPlotter'])
        self.time_list = config['TimeList']
        self.img_name = config['ImgName']
        self.convert_cmd = config['ConvertCommand']
        self.convert_cmd_last = config['ConvertCommandLast']
        gStyle.SetPalette(config['PaletteId'])

    def MakeGIFImage(self, decay_list):
        gStyle.SetOptStat(0)
        for (i,time) in enumerate(self.time_list):
            hist = self.plotter.plotPopulation(decay_list,time)
            hist.SetName("population"+str(i))
            hist.SetTitle("Population at t = "+str(time)+"sec")
            hist.GetXaxis().SetTitle("N")
            hist.GetYaxis().SetTitle("Z")
            hist.Draw("colz")
            gPad.SetLogz()
            gPad.Print(self.img_name + "_%02d.png" % i)
        gPad.Print(self.img_name + "_last.png")

    def MakeGIF(self):
        cmd = self.convert_cmd + " " + self.img_name + "_*.png " \
              + self.convert_cmd_last + " " + self.img_name \
              + "_last.png " + self.img_name + ".gif"
        os.system(cmd) 
