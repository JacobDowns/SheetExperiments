"""
Reference simulation steady state. Trough bed. 10cm bump height. 
"""

from dolfin import *
from dolfin import MPI, mpi_comm_world
from sheet_model import *
from constants import *


### Model inputs

# Process number
MPI_rank = MPI.rank(mpi_comm_world())

model_inputs = {}

prm = NonlinearVariationalSolver.default_parameters()
prm['newton_solver']['relaxation_parameter'] = 1.0
prm['newton_solver']['relative_tolerance'] = 1e-6
prm['newton_solver']['absolute_tolerance'] = 1e-6
prm['newton_solver']['error_on_nonconvergence'] = False
prm['newton_solver']['maximum_iterations'] = 30

pcs['k'] = 4.2e-3
pcs['h_r'] = 0.1
pcs['l_r'] = 0.25
model_inputs['input_file'] = '../inputs_sheet/steady/ref_trough_steady_10cm3.hdf5'
model_inputs['out_dir'] = 'out_ref_trough_steady_hr_10cm3/'
model_inputs['constants'] = pcs
model_inputs['newton_params'] = prm

# Create the sheet model
model = SheetModel(model_inputs)


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
    model.checkpoint(['pfo'])
    
  i += 1
  
model.write_steady_file('../inputs_sheet/steady/ref_trough_steady_10cm3')
