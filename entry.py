''' file that contains the input information for the schedule generator '''
import experiment as exp
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('dir', help='the directory to use for all subsequent importing/exporting')

args = parser.parse_args()
mod_path = f'./ampl-files-{args.dir}'

exp.run_sensitivity_analysis_1(mod_path, (i / 5.0 for i in range(-5, 6)), 30)
exp.run_sensitivity_analysis_2(mod_path, (0.5, 0.4, 0.3, 0.2, 0.1, 0.05), 30)
