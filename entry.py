''' file that contains the input information for the schedule generator '''
import experiment as exp
import argparse
import numpy as np

np.random.seed(1)

parser = argparse.ArgumentParser()
parser.add_argument('dir', help='the directory to use for all subsequent importing/exporting')

args = parser.parse_args()
mod_path = f'./ampl-files-{args.dir}'

if args.dir == 'mod2':
    folder = 'sum_images'
elif args.dir == 'mod3':
    folder = 'maximin_images'

# exp.run_sensitivity_analysis_1(dir, mod_path, (i / 5.0 for i in range(-5, 6)), 30)
# exp.run_sensitivity_analysis_2(dir, mod_path, (0.5, 0.4, 0.3, 0.2, 0.1, 0.05), 30)
exp.run_sensitivity_analysis_3(folder, mod_path, (100, 200, 300, 400, 500), 30)
