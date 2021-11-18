''' file that contains the input information for the schedule generator '''
import experiment as exp

exp.run_sensitivity_analysis_1((i / 5.0 for i in range(-5, 6)), 1)
exp.run_sensitivity_analysis_2((0.5, 0.4, 0.3, 0.2, 0.1, 0.05), 1)
