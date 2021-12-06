''' file that contains the input information for the schedule generator '''
import experiment as exp
import argparse
import numpy as np

np.random.seed(1)

parser = argparse.ArgumentParser()
parser.add_argument('dir', help='the directory to use for all subsequent importing/exporting')

args = parser.parse_args()
mod_path = f'./ampl-files-{args.dir}'

if args.dir == 'mod1':
    folder = 'sum_images'
    lambdas = [0] # dummy variable - is not used in model

elif args.dir == 'mod2':
    folder = 'maximin_images'
    lambdas = [0] # dummy variable - is not used in model

elif args.dir == 'mod3':
    folder = 'combined_images'
    lambdas = [0, 0.25, 0.5, 0.75, 1]

for lamb in lambdas:
    subfolder = f'{folder}/lambda_{lamb}'

    # if there is only one lambda, then don't create subfolders
    if len(lambdas) == 1:
        subfolder = folder

    print(f'Lambda {lamb}')
    exp.run_sensitivity_analysis_1(subfolder, mod_path, (i / 5.0 for i in range(-5, 6)), 30, lamb)
    print()
    exp.run_sensitivity_analysis_2(subfolder, mod_path, (0.5, 0.4, 0.3, 0.2, 0.1, 0.05), 30, lamb)
    print()
    exp.run_sensitivity_analysis_3(subfolder, mod_path, (100, 200, 300, 400, 500), 30, lamb)
    print()
    print()

