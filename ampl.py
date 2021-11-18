from amplpy import AMPL, Environment
import os

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# setup
ampl = AMPL(Environment(os.environ.get('AMPL_PATH')))
ampl.setOption('solver', os.environ.get('SOLVER_PATH'))
ampl.setOption('solver_msg', 0)
print()

def solve_model(mod_path):
    ''' runs the model and returns the DV x '''
    ampl.reset()
    ampl.read(f'{mod_path}/case-study-2.mod')
    ampl.readData(f'{mod_path}/case-study-2.dat')

    if os.path.exists('/dev/null'):
        ampl.eval('solve >/dev/null;')
    else:
        ampl.eval('solve >NUL;')

    return ampl.getData('x;').toList()
    