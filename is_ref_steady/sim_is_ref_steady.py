"""
IS reference simulation steady state.
"""

from dolfin import *
from dolfin import MPI, mpi_comm_world
from sheet_model import *
from constants import *


### Model inputs

# Process number
MPI_rank = MPI.rank(mpi_comm_world())

model_inputs = {}
pcs['k'] = 5e-3
model_inputs['input_file'] = '../inputs_sheet/inputs_is/inputs_is.hdf5'
model_inputs['out_dir'] = 'out_is_ref/'
model_inputs['constants'] = pcs

# Create the sheet model
model = SheetModel(model_inputs)


### Run the simulation

# Seconds per day
spd = pcs['spd']
# End time
T = 100.0 * spd
# Time step
dt = spd / 3.0
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
  
model.write_steady_file('out_is_ref/ref_steady_is')