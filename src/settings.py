class Settings:
        def __init__(self):
                self.avg = 200000
                self.coverage = 1
                self.fprate = 1.0 #number of fp in 100kb
                self.bns_version = '0.1'
                self.bnx_version = '1.2'
                self.fnrate = 0.15 #fn rate of true labels
                self.chimrate = 0.01 #rate of chimeric reads
                self.sd = 1500 #sd of knick position
                #TODO stretchfactor = .85
                #TODO bp per chip
