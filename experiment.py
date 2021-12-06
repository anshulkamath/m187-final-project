from ampl import solve_model
import matplotlib.pyplot as plt
import numpy as np
import os
from pandas.core.frame import DataFrame
import seaborn as sns

from classes.ClassManager import Class
from classes.Student import Schedule
from constants import *
import utils
    
def create_df(ampl_output, prefs):
    df_dict = {}
    cols = sorted([section for c in classes for section in c.get_sections()])

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
    num_sections = len([section for c in classes for section in c.get_sections()])

    # number of people for each level of happiness
    happiness = np.zeros((5,5))

    # create dictionary
    for i in range(0, len(ampl_output), num_sections):
        student = ampl_output[i][0]
        curr_prefs = prefs[int(student)]['preferences']
        class_idx = np.where(np.array(ampl_output[i:i+num_sections])[:,3] == '1.0')[0]
        
        if len(class_idx) == 0:
            happiness[0,0] += 1
        elif len(class_idx) == 1:  # assume it's an elective
            happiness[0,curr_prefs[class_idx[0]] + 1] += 1
        elif len(class_idx) == 2:  # assume 1 req and 2 elect preplacement, and req comes first in list
            happiness[curr_prefs[class_idx[0]] + 1, curr_prefs[class_idx[1]] + 1] += 1

    return happiness / (len(ampl_output) / num_sections)

def create_heatmap(data):
    data = np.flipud(data)
    sns.heatmap(data, cmap='rocket_r', vmin=0, vmax=1.0)
    plt.xlabel("Happiness with Elective Class")
    plt.ylabel("Happiness with Required Class")
    plt.xticks(np.arange(5)+0.5, ["N/A", "NO", "OPEN", "INT", "YAY"])
    plt.yticks(np.arange(5)+0.5, ["N/A", "NO", "OPEN", "INT", "YAY"][::-1])

def run_experiment(mod_path, matrix = None, sensitivity = 0, sdev = 0.3, num_students = 210, lamb=0):
    '''
    runs a single experiment, tabulating results in
    given matrix and using given sensitivity
    '''
    # adjust params as necessary
    if sensitivity:
        old_sensitivity = Class.get_sensitivity()
        Class.adjust_sensitivity(sensitivity)

    if sdev:
        old_sigma = Schedule.get_sigma()
        Schedule.adjust_sigma(sdev)

    prefs = utils.generate_dat(mod_path, num_students=num_students, lamb=lamb)
    x_soln = solve_model(mod_path)

    if matrix is not None:
        matrix += create_matrix(x_soln, prefs)
    
    # revert changes
    if sensitivity:
        Class.adjust_sensitivity(old_sensitivity)

    if sdev:
        Schedule.adjust_sigma(old_sigma)

    return x_soln

def check_dir(path):
    subdirs = path.split('/')

    for i in range(1, len(subdirs)):
        curr_dir = '/'.join(subdirs[:i+1])
        if not os.path.exists(curr_dir):
            os.mkdir(curr_dir)

def run_sensitivity_analysis_1(dir, mod_path, sensitivities, num_trials = 30, lamb=0):
    ''' runs sensitivity analysis with the given params '''
    directory = f'./{dir}/sa1'

    check_dir(directory)
    
    for sensitivity in sensitivities:
        print(f'Creating heatmap with sensitivity: {sensitivity}')
        plt.figure()

        matrix = np.zeros((5,5))
        for _ in range(num_trials):
            run_experiment(mod_path, matrix, sensitivity = sensitivity, lamb = lamb)
        
        create_heatmap(matrix / num_trials)
        file_name = str(abs(sensitivity))
        file_name = ('neg_' if sensitivity < 0 else 'pos_') + file_name

        plt.savefig(f'{directory}/heatmap_{file_name}.png')
        plt.close()

def run_sensitivity_analysis_2(dir, mod_path, stdevs, num_trials = 30, lamb=0):
    ''' runs sensitivity analysis with the given params '''
    directory = f'./{dir}/sa2'

    check_dir(directory)
    
    for stdev in stdevs:
        print(f'Creating heatmap with standard deviation: {stdev}')
        plt.figure()

        matrix = np.zeros((5,5))
        for _ in range(num_trials):
            run_experiment(mod_path, matrix, sdev = stdev, lamb=lamb)
        
        create_heatmap(matrix / num_trials)
        file_name = str(stdev)

        plt.savefig(f'{directory}/heatmap_{file_name}.png')
        plt.close()


def run_sensitivity_analysis_3(dir, mod_path, num_students, num_trials = 30, lamb=0):
    ''' runs sensitivity analysis with the given params '''
    directory = f'./{dir}/sa3'

    check_dir(directory)
    
    for students in num_students:
        print(f'Creating heatmap with {students} students')
        plt.figure()

        matrix = np.zeros((5,5))
        for _ in range(num_trials):
            run_experiment(mod_path, matrix, num_students=students, lamb=lamb)
        
        create_heatmap(matrix / num_trials)
        file_name = str(students)

        plt.savefig(f'{directory}/heatmap_{file_name}.png')
        plt.close()
