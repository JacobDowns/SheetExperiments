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

pt1 = PlotTools('out_trough_sliding_only_hr_2m/out.hdf5')
#pt2 = PlotTools('out_trough_sliding_only_hr_1m1/out.hdf5')
#pt3 = PlotTools('out_trough_sliding_only_hr_1m2/out.hdf5')

matplotlib.rcParams.update({'font.size': 18})
matplotlib.rcParams['mathtext.default']='regular'

def get_pressures(pt):
  avg = []
  ts = []
  
  for i in range(pt.num_steps):
    ts.append(pt.get_t(i))
    avg.append(pt.get_avg_pfo(i))

  return array(ts), array(avg)


pfos1 = get_pressures(pt1)
#pfos2 = get_pressures(pt2)
#pfos3 = get_pressures(pt3)

print (0.8 - min(pfos1[1])) / 0.8

ts = pfos1[0] / pcs['spm']

plot(ts, pfos1[1], 'k', linewidth = 2)
#plot(ts, pfos2[1], 'k--', linewidth = 2)
#plot(ts, pfos3[1], 'k:', linewidth = 2)
ylim([0.6, 0.9])
grid(True)

show()

  