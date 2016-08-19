"""
Reference simulation steady state.
"""

from dolfin import *
from dolfin import MPI, mpi_comm_world
from sheet_model import *
from constants import *

### Model inputs

# Process number 
MPI_rank = MPI.rank(mpi_comm_world())
# Model inputs are passed into the SheetModel object using this model_inputs dictionary
model_inputs = {}
# Path of the hdf5 file with model inputs
model_inputs['input_file'] = '../inputs_sheet/inputs/inputs_high.hdf5'
model_inputs['out_dir'] = 'out_ref_steady/'
# Create the sheet model object
model = SheetModel(model_inputs)


### Run the simulation

# Seconds per day
spd = pcs['spd']
# Simulate end time
T = 90.0 * spd
# Time step
dt = spd / 2.0

while model.t < T:
  # First process prints current model time  
  if MPI_rank == 0: 
    current_time = model.t / spd
    print ('%sCurrent time: %s %s' % (fg(1), current_time, attr(0)))
  
  # Advance the model by the time step
  model.step(dt)
  # Ouput paraview files with pressure (pfo) and sheet height h
  model.write_pvds(['pfo', 'h'])
  
# Write a steady state file
model.write_steady_file('../inputs_sheet/steady/ref_steady')
