# PopulationGIFMaker.py generated by R. Yokoyama on 10/05/2018
from PopulationPlotter import PopulationPlotter
import ROOT
import os
import copy

class PopulationGIFMaker(object):
    # A class to make a gif animation of nuclear population
    # from a given list of decay chains
    def __init__(self):
        self.plotter = PopulationPlotter()
        self.time_list = []
        self.log_y = False

    def configure(self, config):
        # initialize variables by a given yaml node
        self.plotter.configure(config['PopulationPlotter'])
        self.time_list = config['TimeList'] # a list of time to make the animation
        self.img_name = config['ImgName'] # a prefix of the image file names
        self.convert_cmd = config['ConvertCommand'] # "convert -layers optimize -loop 0 -delay xx" for example
        self.convert_cmd_last = config['ConvertCommandLast'] # put "-delay xx" if you want to make the last image longer
        self.log_y = bool(config['Logy']) # Log scale on Y axis
        ROOT.gStyle.SetPalette(config['PaletteId']) # ROOT palette ID

    def MakeGIFImage(self, decay_list):
        # print the population images at the times which are specified
        # in the self.time_list
        ROOT.gStyle.SetOptStat(0)
        for (i,time) in enumerate(self.time_list):
            hist = self.plotter.plotPopulation(decay_list,time)
            hist.SetName("population"+str(i))
            hist.SetTitle("Population at t = "+str(time)+"sec")
            hist.GetXaxis().SetTitle("N")
            hist.GetYaxis().SetTitle("Z")
            hist.Draw("colz")
            ROOT.gPad.SetLogz()
            ROOT.gPad.Print(self.img_name + "_%02d.png" % i)
        ROOT.gPad.Print(self.img_name + "_last.png")

    def MakePATHGIFImage(self, decay_list):
        # print the population images at the times which are specified
        # in the self.time_list
        ROOT.gStyle.SetOptStat(0)
        label = ROOT.TText()
        label.SetTextColor(2)
        label.SetTextAlign(23)
        label.SetTextSize(0.05)
        label.SetNDC(1)
        hist_b = self.plotter.plotPopulation(decay_list,0)
        for (i,time) in enumerate(self.time_list):
            hist = self.plotter.plotPopulation(decay_list,time)
            hist.SetName("population"+str(i))
          
            for chain in decay_list:
                nucl_before = filter(lambda x: x.time < time, chain.event_list)
                if len(nucl_before) == 0:
                    hist_b.Fill(chain.event_list[0].n,chain.event_list[0].z)
                else:
                    for event in nucl_before:
                        hist_b.Fill(event.n,event.z)
   
            n_populated = 0
            for ix in range(0,hist_b.GetNbinsX()):
                for iy in range(0,hist_b.GetNbinsY()):
                    if hist_b.GetBinContent(ix,iy) > 0:
                        hist_b.SetBinContent(ix,iy,10)
                        n_populated = n_populated + 1
            hist_b.SetMinimum(0)
            hist_b.SetMaximum(10)
            hist_b.SetFillColor(4)
            hist_b.SetFillStyle(3001)
            hist_b.SetTitle("Population at t = "+str(time)+"sec")
            hist_b.GetXaxis().SetTitle("N")
            hist_b.GetYaxis().SetTitle("Z")
            hist_b.GetXaxis().SetLabelSize(0.05)
            hist_b.GetYaxis().SetLabelSize(0.05)
            hist_b.GetZaxis().SetLabelSize(0.05)
            hist_b.GetXaxis().SetTitleSize(0.05)
            hist_b.GetYaxis().SetTitleSize(0.05)
            hist_b.GetYaxis().SetNdivisions(505)
            hist_b.Draw("box")
            hist.Draw("colz same")
            if self.log_y:
                ROOT.gPad.SetLogz()
            label.DrawText(0.5,0.88,"number of nuclides populated: "+str(n_populated))
            ROOT.gPad.Print(self.img_name + "_%02d.png" % i)
        ROOT.gPad.Print(self.img_name + "_last.png")
        ROOT.gPad.Print(self.img_name + "_last.eps")

    def MakePATHGIFImage2(self, decay_list1, decay_list2, name1, name2):
        # print the population images at the times which are specified
        # in the self.time_list
        ROOT.gStyle.SetOptStat(0)
        label = ROOT.TText()
        label.SetTextColor(2)
        label.SetTextAlign(23)
        label.SetTextSize(0.05)
        label.SetNDC(1)
        hist_b = self.plotter.plotPopulation(decay_list1,0)
        hist_b2 = self.plotter.plotPopulation(decay_list2,0)
        for (i,time) in enumerate(self.time_list):
            hist = self.plotter.plotPopulation(decay_list1,time)
            hist.SetName("population"+str(i))
          
            for chain in decay_list1:
                nucl_before = filter(lambda x: x.time < time, chain.event_list)
                if len(nucl_before) == 0:
                    hist_b.Fill(chain.event_list[0].n,chain.event_list[0].z)
                else:
                    for event in nucl_before:
                        hist_b.Fill(event.n,event.z)
   
            n_populated = 0
            for ix in range(0,hist_b.GetNbinsX()):
                for iy in range(0,hist_b.GetNbinsY()):
                    if hist_b.GetBinContent(ix,iy) > 0:
                        hist_b.SetBinContent(ix,iy,10)
                        n_populated = n_populated + 1
            hist_b.SetMinimum(0)
            hist_b.SetMaximum(10)
            hist_b.SetFillColor(4)
            hist_b.SetFillStyle(3004)
            hist_b.SetTitle("Population at t = "+str(time)+"sec")
            hist_b.GetXaxis().SetTitle("N")
            hist_b.GetYaxis().SetTitle("Z")
            hist_b.Draw("box")
            hist.Draw("colz same")
            ROOT.gPad.SetLogz()
            label.DrawText(0.5,0.88,name1)
            ROOT.gPad.Print(self.img_name + "_%02d.png" % i)

        for (i,time) in enumerate(self.time_list):
            hist = self.plotter.plotPopulation(decay_list2,time)
            hist.SetName("population"+str(i))
          
            for chain in decay_list2:
                nucl_before = filter(lambda x: x.time < time, chain.event_list)
                if len(nucl_before) == 0:
                    hist_b2.Fill(chain.event_list[0].n,chain.event_list[0].z)
                else:
                    for event in nucl_before:
                        hist_b2.Fill(event.n,event.z)
   
            n_populated = 0
            for ix in range(0,hist_b2.GetNbinsX()):
                for iy in range(0,hist_b2.GetNbinsY()):
                    if hist_b2.GetBinContent(ix,iy) > 0:
                        hist_b2.SetBinContent(ix,iy,10)
                        n_populated = n_populated + 1
            hist_b2.SetMinimum(0)
            hist_b2.SetMaximum(10)
            hist_b2.SetFillColor(2)
            hist_b2.SetFillStyle(3005)
            hist_b2.SetTitle("Population at t = "+str(time)+"sec")
            hist_b2.GetXaxis().SetTitle("N")
            hist_b2.GetYaxis().SetTitle("Z")
            ROOT.gPad.Clear()
            ROOT.gPad.SetLogz(0)
            hist_b.Draw("box")
            hist_b2.Draw("box same")
            hist.Draw("colz same")
            #ROOT.gPad.SetLogz()
            label.DrawText(0.5,0.88,name2)
            ROOT.gPad.Print(self.img_name + "_%02d.png" % (i+len(self.time_list)))

        ROOT.gPad.Print(self.img_name + "_last.png")


    def MakeRatioGIFImage(self, decay_list1, decay_list2, name1, name2):
        # print the ratio of the population images at the times which are specified
        # in the self.time_list
        ROOT.gStyle.SetOptStat(0)
        for (i,time) in enumerate(self.time_list):
            hist1 = copy.copy(self.plotter.plotPopulation(decay_list1,time))
            hist1.SetName("population1"+str(i))
            hist1.SetTitle("Population("+name1+"/"+name2+") at t = "+str(time)+"sec")
            hist1.GetXaxis().SetTitle("N")
            hist1.GetYaxis().SetTitle("Z")
            hist2 = copy.copy(self.plotter.plotPopulation(decay_list2,time))
            hist2.SetName("population2"+str(i))
            hist2.Add(hist1)
            hist1.Divide(hist2)
            hist1.SetMinimum(0)
            hist1.SetMaximum(1)
            hist1.Draw("colz")
            ROOT.gPad.Print(self.img_name + "_%02d.png" % i)
        ROOT.gPad.Print(self.img_name + "_last.png")

    def Make2DandAGIFImage(self, decay_list1, decay_list2, name1, name2):
        # print the 1D population images at the times which are specified
        # in the self.time_list
        ROOT.gStyle.SetOptStat(0)
        canv = ROOT.TCanvas("population","population",1200,740)
            
        for (i,time) in enumerate(self.time_list):
            canv.Clear()
            canv.Divide(1,2)
            pad2 = canv.cd(2)
            pad1 = canv.cd(1)
            pad1.Divide(2,1)
            pad1_2 = pad1.cd(2)
            pad1_1 = pad1.cd(1)

            hist1 = self.plotter.plotPopulation(decay_list1,time)
            hist1.SetName("population_"+name1+str(i))
            hist1.SetTitle("Population "+name1+" at t = "+str(time)+"sec")
            hist1.GetXaxis().SetTitle("N")
            hist1.GetYaxis().SetTitle("Z")
            hist1.Draw("colz")
            if self.log_y:
                pad1_1.SetLogz()

            pad1.cd(2)
            hist2 = self.plotter.plotPopulation(decay_list2,time)
            hist2.SetName("population_"+name2+str(i))
            hist2.SetTitle("Population "+name2+" at t = "+str(time)+"sec")
            hist2.GetXaxis().SetTitle("N")
            hist2.GetYaxis().SetTitle("Z")
            hist2.Draw("colz")
            if self.log_y:
                pad1_2.SetLogz()

            canv.cd(2)
            hist3 = self.plotter.plotPopulationA(decay_list1,time)
            hist3.SetName("populationA_"+name1+str(i))
            hist3.SetTitle("PopulationA "+name1+" at t = "+str(time)+"sec")
            hist3.GetXaxis().SetTitle("A")
            hist3.SetLineColor(2)
            hist3.Draw()
            hist4 = self.plotter.plotPopulationA(decay_list2,time)
            hist4.SetName("populationA_"+name2+str(i))
            hist4.SetTitle("PopulationA "+name2+" at t = "+str(time)+"sec")
            hist4.GetXaxis().SetTitle("A")
            hist4.Draw("same")
            if self.log_y:
                pad2.SetLogy()
            pad2.BuildLegend(0.7,0.8,0.98,0.98)

            canv.Print(self.img_name + "_%02d.png" % i)
        canv.Print(self.img_name + "_last.png")

    def Make1DGIFImage(self, decay_list1, decay_list2, name1, name2):
        # print the 1D population images at the times which are specified
        # in the self.time_list
        ROOT.gStyle.SetOptStat(0)
        canv = ROOT.TCanvas("population","population",1200,1920)
            
        for (i,time) in enumerate(self.time_list):
            hists1 = self.plotter.plotPopulation1D(decay_list1,time)
            canv.Clear()
            canv.Divide(1,len(hists1))
            label = ROOT.TText()
            label.SetTextColor(2)
            label.SetTextAlign(13)
            label.SetTextSize(0.3)
            label.SetNDC(1)
            j = 0
            for key in hists1:
                j = j+1
                pad = canv.cd(j)
                if self.log_y:
                    pad.SetLogy()
                    hists1[key].SetMinimum(1)
                hists1[key].SetName("population"+str(i)+"_"+str(key)+name1)
                hists1[key].SetTitle("Population at t = "+str(time)+"sec, z = "+str(key)+" "+name1)
                hists1[key].GetXaxis().SetTitle("N")
                hists1[key].GetYaxis().SetTitle("counts")
                hists1[key].SetLineColor(2)
                hists1[key].Draw()
            hists2 = self.plotter.plotPopulation1D(decay_list2,time)
            j = 0
            for key in hists2:
                j = j+1
                pad = canv.cd(j)
                if self.log_y:
                    hists2[key].SetMinimum(1)
                hists2[key].SetName("population"+str(i)+"_"+str(key)+name2)
                hists2[key].SetTitle("Population at t = "+str(time)+"sec, z = "+str(key)+" "+name2)
                hists2[key].GetXaxis().SetTitle("N")
                hists2[key].GetYaxis().SetTitle("counts")
                hists2[key].SetLineColor(4)
                hists2[key].Draw("same")
                label.DrawText(0,1,"z = "+str(key))
            canv.cd(1)
            label.SetTextAlign(33)
            label.DrawText(1,1,"t = "+str(time)+"sec")
            label.SetTextAlign(31)
            label.DrawText(1,0.5,"red:beoh")
            label.SetTextColor(4)
            label.SetTextAlign(33)
            label.DrawText(1,0.5,"blue:old")
            canv.Print(self.img_name + "_%02d.png" % i)
        canv.Print(self.img_name + "_last.png")

    def MakeGIF(self):
        # generates .gif file using "convert" command
        cmd = self.convert_cmd + " " + self.img_name + "_*.png " \
              + self.convert_cmd_last + " " + self.img_name \
              + "_last.png " + self.img_name + ".gif"
        os.system(cmd) 
