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
    
    
def create_df(ampl_output, prefs):
    df_dict = {}
    cols = sorted([section for c in ent.classes for section in c.get_sections()])

    # create dictionary
    for (student, _, _, is_taking) in ampl_output:
        student = round(float(student))

        if student not in df_dict:
            df_dict[student] = []
        
        df_dict[student].append(is_taking)

    # convert dictionary to numpy and take product with prefs
    for key in df_dict:
        curr_prefs = prefs[key]['preferences']

        # normalize wrt the highest 
        df_dict[key] = np.array(df_dict[key]) * np.array(curr_prefs) / max(curr_prefs)

    df = DataFrame.from_dict(df_dict, orient='index', dtype=np.uint16, columns=cols)

    return df


def create_matrix(ampl_output, prefs):
    num_sections = len([section for c in ent.classes for section in c.get_sections()])

    # number of people for each level of happiness
    happiness = np.zeros((5,5))

    # create dictionary
    for i in range(0, len(ampl_output), num_sections):
        student = ampl_output[i][0]
        curr_prefs = prefs[int(student)]['preferences']
        class_idx = np.where(np.array(ampl_output[i:i+num_sections])[:,3] == '1.0')
        
#         len(class_idx[0]) == 0?
        if len(class_idx[0]) == 1:  # assume it's an elective
#             elect_happiness[curr_prefs[class_idx[0][0]]] += 1
            happiness[4,curr_prefs[class_idx[0][0]]] += 1
        elif len(class_idx[0]) == 2:  # assume 1 req and 2 elect preplacement, and req comes first in list
            # INVALID! ex. CS124 and CS131
#             req_happiness[curr_prefs[class_idx[0][0]]] += 1
#             elect_happiness[curr_prefs[class_idx[0][1]]] += 1
            happiness[curr_prefs[class_idx[0][0]], curr_prefs[class_idx[0][1]]] += 1

    # normalize the number of students --> a percentage
#     req_happiness, elect_happiness = np.array(req_happiness), np.array(elect_happiness)
#     print(np.sum(req_happiness), np.sum(elect_happiness))
#     print(req_happiness, elect_happiness)
#     req_happiness = req_happiness / np.sum(req_happiness)
#     elect_happiness = elect_happiness / np.sum(elect_happiness)
#     print(req_happiness, elect_happiness)
#     return np.array(req_happiness).reshape((-1,1)) + np.array(elect_happiness).reshape((1,-1)) / 2
    return happiness



def create_heatmap(data):
    data = np.flipud(data)
    ax = sns.heatmap(data, cmap='BuPu', cbar_kws={'label': 'Number of Students'}, annot=True)
    plt.xlabel("Happiness with Required Class")
    plt.ylabel("Happiness with Elective Class")
    plt.xticks(np.arange(5)+0.5, ["NO", "OPEN", "INT", "YAY", "N/A"])
    plt.yticks(np.arange(5)+0.5, ["NO", "OPEN", "INT", "YAY", "N/A"][::-1])
    plt.show()

for i in range(1):
    prefs = ent.generate_dat()
    
    solve_model()

    x_soln = ampl.getData('x;').toList()
    df = create_df(x_soln, prefs)
#     df.to_html('output.html')
    matrix = create_matrix(x_soln, prefs)
    create_heatmap(matrix)
