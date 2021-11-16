from amplpy import AMPL, Environment
import entry as ent
import numpy as np
from pandas.core.frame import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# setup
ampl = AMPL(Environment('../../'))
ampl.setOption('solver', '../../gurobi')
ampl.setOption('solver_msg', 0)
ampl.setOption('outlev', 0)

def solve_model():
    ''' runs the model '''
    ampl.reset()
    ampl.read('ampl-files/case-study-2.mod')
    ampl.readData('ampl-files/case-study-2.dat')
    ampl.eval('solve >/dev/null;')

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

def get_heatmap_data(df: DataFrame):
    students = []
    data_low = {}
    data_high = {}

    for row in df.index:
        row = df.loc[row].to_numpy()
        appendee = sorted(row[np.nonzero(row)], reverse=True)

        if len(appendee) == 1:
            appendee.append(0)
            appendee.reverse()

        students.append(appendee if appendee else [0, 0])
    
    for [low, high] in students:
        if low not in data_low:
            data_low[low] = 0
        data_low[low] += 1

        if high not in data_high:
            data_high[high] = 0
        data_high[high] += 1

        # enforcing consistent shapes
        if low not in data_high:
            data_high[low] = 0

        if high not in data_low:
            data_low[high] = 0

    ret = []; labels = []
    for data in [data_low, data_high]:
        acc_labels = []
        acc_ret = []
        for key in sorted(data.keys()):
            acc_labels.append(key)
            acc_ret.append(data[key])
        
        labels.append(acc_labels)
        ret.append(acc_ret)

    return DataFrame(ret, columns=labels[0], index=labels[1])

def create_heatmap(data: DataFrame):
    ax = sns.heatmap(data)
    plt.show()

for i in range(1):
    prefs = ent.generate_dat()
    
    solve_model()

    x_soln = ampl.getData('x;').toList()
    df = create_df(x_soln, prefs)
    create_heatmap(get_heatmap_data(df))
