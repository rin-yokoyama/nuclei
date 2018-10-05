import ROOT

class EventPlotter:
    def __init__(self, config_yaml):
        self.config = config_yaml
        self.hist_list = []
        h_config = self.config['n_decay']
        self.hist_list.append(ROOT.TH1D("n_decay","n_decay",int(h_config['nbins']),float(h_config['low']),float(h_config['up'])))
        h_config = self.config['decay_activity']
        self.hist_list.append(ROOT.TH1D("decay_activity","decay_activity",int(h_config['nbins']),float(h_config['low']),float(h_config['up'])))
        h_config = self.config['n_ave']
        self.hist_list.append(ROOT.TH1D("n_ave","n_ave",h_config['nbins'],h_config['low'],h_config['up']))

    def fillDecays(self,decay_list):
        h_n_decay = filter(lambda x: x.GetName() == "n_decay",self.hist_list)[0]
        h_decay_time = filter(lambda x: x.GetName() == "decay_activity",self.hist_list)[0]
        h_n_ave = filter(lambda x: x.GetName() == "n_ave",self.hist_list)[0]
        for decay in decay_list:
            h_n_decay.Fill(len(decay.event_list))
            n_neutron = 0
            for event in decay.event_list:
                h_decay_time.Fill(event.time)
                n_neutron = n_neutron + event.n_neutron
            h_n_ave.Fill(n_neutron)

    def writeHistograms(self):
        for hist in self.hist_list:
            hist.Write()

