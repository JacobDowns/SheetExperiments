"""
IS winter simulation where conductivity remains constant but sliding
decreases. 
"""

from dolfin import *
from dolfin import MPI, mpi_comm_world
from sheet_model import *
from constants import *
from scale_functions import *


# Process number
MPI_rank = MPI.rank(mpi_comm_world())

# Scale functions for determining winter sliding speed
input_file = '../inputs_sheet/steady_is/ref_steady_is.hdf5'
scale_functions = ScaleFunctions(input_file, 5e-3, 5e-3, u_b_max = 100.0)

model_inputs = {}
model_inputs['input_file'] = input_file
model_inputs['out_dir'] = 'out_is_sliding_only/'
model_inputs['constants'] = pcs
model_inputs['opt_params'] = {'tol' : 5e-3, 'scale' : 30}

# Create the sheet model
model = SheetModel(model_inputs)


### Run the simulation

# Seconds per month
spm = pcs['spm']
# Seconds per day
spd = pcs['spd']
# End time
T = 8.0 * spm
# Time step
dt = spd / 3.0
# Iteration count
i = 0

while model.t < T:  
  # Update the melt
  model.set_m(scale_functions.get_m(model.t))
  # Update the sliding speed
  model.set_u_b(scale_functions.get_u_b(model.t))  
  
  if MPI_rank == 0: 
    current_time = model.t / spd
    print ('%sCurrent time: %s %s' % (fg(1), current_time, attr(0)))
  
  model.step(dt)
  
  if i % 1 == 0:
    model.write_pvds(['pfo', 'h'])
    
  if i % 1 == 0:
    model.checkpoint(['m', 'pfo', 'h', 'u_b', 'k'])
  
  if MPI_rank == 0: 
    print
    
  i += 1