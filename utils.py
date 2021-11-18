import numpy as np
from classes.Exporter import Exporter
from constants import *

def generate_dat(export_path):
    num_students = 300
    exporter = Exporter(
        classes,
        years,
        reg_times,
        happiness,
        num_students,
        class_times
    )

    return exporter.write_dat_file(f'{export_path}/case-study-2.dat', np.random.choice(['CS', 'CSM'], num_students, p=[0.5, 0.5]), req_majors)