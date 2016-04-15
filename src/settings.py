class Settings:
        def __init__(self):
                self.avg = 200000
                self.coverage = 100
                self.fprate = 1.0 #number of fp in 100kb
                self.bns_version = '0.1'
                self.bnx_version = '1.2'
                self.fnrate = 0.15 #fn rate of true labels
                self.chimrate = 0.01 #rate of chimeric reads
                self.sd = 50 #sd of knick position
                self.fragile_same = 50
                self.fragile_opposite = 150
                self.fragile_treshold = 25
                self.fragile_factor = 3
                #TODO stretchfactor = .85
                self.chip_size = 10000000000 # 10 Gbp
