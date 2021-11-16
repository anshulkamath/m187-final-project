from amplpy import AMPL, Environment
import entry as ent
import numpy as np
from pandas.core.frame import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# setup
ampl = AMPL(Environment('../ampl_mswin64/ampl_mswin64/'))
ampl.setOption('solver', '../ampl_mswin64/ampl_mswin64/gurobi')
ampl.setOption('solver_msg', 0)
ampl.setOption('outlev', 0)

def solve_model():
    ''' runs the model '''
    ampl.reset()
    ampl.read('ampl-files/case-study-2.mod')
    ampl.readData('ampl-files/case-study-2.dat')
#     ampl.eval('solve >/dev/null;')
    ampl.solve()


def create_matrix(ampl_output, prefs):
    num_sections = len([section for c in ent.classes for section in c.get_sections()])

    # number of people for each level of happiness
    req_happiness, elect_happiness = [0,0,0,0], [0,0,0,0]

    # create dictionary
    for i in range(0, len(ampl_output), num_sections):
        student = ampl_output[i][0]
        curr_prefs = prefs[int(student)]['preferences']
        class_idx = np.where(np.array(ampl_output[i:i+num_sections])[:,3] == '1.0')
        
        if len(class_idx[0]) == 1:  # assume it's an elective
            elect_happiness[curr_prefs[class_idx[0][0]]] += 1
        else:  # assume 1 req and 2 elect preplacement, and req comes first in list
            req_happiness[curr_prefs[class_idx[0][0]]] += 1
            elect_happiness[curr_prefs[class_idx[0][1]]] += 1

    return np.array(req_happiness).reshape((-1,1)) + np.array(elect_happiness).reshape((1,-1))



def create_heatmap(data: DataFrame):
    ax = sns.heatmap(data, cmap='BuPu', cbar_kws={'label': 'Number of Students'})
    plt.xlabel("Happiness with Required Class")
    plt.ylabel("Happiness with Elective Class")
    plt.show()

for i in range(1):
    prefs = ent.generate_dat()
    
    solve_model()

    x_soln = ampl.getData('x;').toList()
    matrix = create_matrix(x_soln, prefs)
    create_heatmap(matrix)
