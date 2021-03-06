"""
Winter simulation on a trough bed where conductivity remains constant but sliding
decreases. Bump height 2m.
"""

from dolfin import *
from dolfin import MPI, mpi_comm_world
from sheet_model import *
from constants import *
from scale_functions import *


# Process number
MPI_rank = MPI.rank(mpi_comm_world())

# Scale functions for determining winter sliding speed
input_file = '../inputs_sheet/steady/ref_trough_steady_2m.hdf5'
scale_functions = ScaleFunctions(input_file,  2e-4,  2e-4, u_b_max = 100.0)

prm = NonlinearVariationalSolver.default_parameters()
prm['newton_solver']['relaxation_parameter'] = 1.0
prm['newton_solver']['relative_tolerance'] = 1e-7
prm['newton_solver']['absolute_tolerance'] = 1e-7
prm['newton_solver']['error_on_nonconvergence'] = False
prm['newton_solver']['maximum_iterations'] = 30

model_inputs = {}
pcs['k'] = 2e-4
pcs['h_r'] = 2.0
pcs['l_r'] = 5.0
model_inputs['input_file'] = input_file
model_inputs['out_dir'] = 'out_trough_sliding_only_hr_2m/'
model_inputs['constants'] = pcs
model_inputs['newton_params'] = prm

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
dt = 60.0 * 60.0 * 4.0
# Iteration count
i = 0

while model.t < T:  
  # Update the melt
  model.set_m(scale_functions.get_m(model.t))
  # Update the sliding speed
  model.set_u_b(project(scale_functions.get_u_b(model.t), model.V_cg))  
  
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
