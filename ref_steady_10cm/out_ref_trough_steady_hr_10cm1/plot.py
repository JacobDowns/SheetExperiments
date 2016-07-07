# -*- coding: utf-8 -*-
"""
Plot reference experiments where sliding decreases but nothing else.
"""
from dolfin import *
from plot_tools import *
from pylab import *
from constants import *

#plot_tools1 = PlotTools('out_sliding_only.hdf5')
#plot_tools2 = PlotTools('out_trough_sliding_only.hdf5')

plot_tools1 = PlotTools('out.hdf5')

matplotlib.rcParams.update({'font.size': 18})
matplotlib.rcParams['mathtext.default']='regular'

def get_pressures(pt):
  avg = []
  ts = []
  
  for i in range(pt.num_steps):
    ts.append(pt.get_t(i))
    avg.append(pt.get_avg_pfo(i))

  return array(ts), array(avg)


pfos = get_pressures(plot_tools1)


ts = pfos[0] / pcs['spm']

plot(ts, pfos[1], 'r', linewidth = 2, label = "1 Flat")
grid(True)

show()

  