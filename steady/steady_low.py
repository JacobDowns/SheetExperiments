"""
Steady state for the trough with a spatially varying k. Low melt.
"""

from dolfin import *
from dolfin import MPI, mpi_comm_world
from sheet_model import *
from constants import *
from scale_functions import *


### Model inputs

# Process number
MPI_rank = MPI.rank(mpi_comm_world())

model_inputs = {}
input_file = '../inputs_sheet/inputs/inputs_trough_low.hdf5'
scale_functions = ScaleFunctions(input_file, 5e-5, 5e-3, u_b_max = 100.0)
model_inputs['input_file'] = input_file
model_inputs['out_dir'] = 'out_trough_steady_low/'
model_inputs['constants'] = pcs

# Create the sheet model
model = SheetModel(model_inputs)
model.set_k(scale_functions.get_k(0.0))

### Run the simulation

# Seconds per day
spd = pcs['spd']
# End time
T = 100.0 * spd
# Time step
dt = spd
# Iteration count
i = 0

while model.t < T:  
  if MPI_rank == 0: 
    current_time = model.t / spd
    print ('%sCurrent time: %s %s' % (fg(1), current_time, attr(0)))
  
  model.step(dt)
  
  if i % 1 == 0:
    model.write_pvds(['pfo', 'h'])
    
  i += 1
  
model.write_steady_file('../inputs_sheet/steady/trough_steady_low')