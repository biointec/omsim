
import sys
import random
from math import exp, sqrt, log, fabs, floor, pi
from numpy.random import seed as nprseed
from scipy.stats import invgamma, nbinom, norm, describe

kbp = 1000
mbp = 1000 * kbp
gbp = 1000 * mbp

class Noise:
        def __init__(self, mml, avg, sd):
                self.seed = 0
                self.min_mol_len = mml
                self.avg_mol_len = avg
                self.sd_mol_len = sd
                self.m_size = []
                self.m_size_idx = -1
                self.m_size_len = 0
                self.sum = 0
                self.sampled = 0.0
                self.succes = 0.0
                # set seeds
                random.seed(self.seed)
                nprseed(self.seed)
                self.sizefile = open('size.out', 'w')
        
        def gen(self):
                # simulate 100 gbp
                while self.sum < 100 * gbp:
                        x = self.next_m_size()
                        self.sampled += 1
                        if x > self.min_mol_len:
                                self.succes += 1
                                self.sum += x
                                self.sizefile.write(str(x) + '\n')
                print("{0:.2f}".format(100 * self.succes / self.sampled) + "% of samples were sufficiently long.")
        
        def randnegbinom(self, mu, sd, size):
                mu = float(mu)
                sd = float(sd)
                r = (mu * mu) / (sd * sd - mu)
                p = 1 - mu / (r + mu)
                result = nbinom.rvs(r, p, size=size)
                return result
        
        def next_m_size(self):
                self.m_size_idx += 1
                if self.m_size_idx == self.m_size_len:
                        self.m_size = self.randnegbinom(self.avg_mol_len, self.sd_mol_len, 100000)
                        self.m_size_idx = 0
                        self.m_size_len = len(self.m_size)
                return self.m_size[self.m_size_idx]

argv = sys.argv
noise = Noise(int(argv[1]) * kbp, int(argv[2]) * kbp, int(argv[3]) * kbp)
noise.gen()
