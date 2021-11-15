''' file that contains the input information for the schedule generator '''
from ClassManager import Class
from Export import Export
import numpy as np

class_times = [
    '8:00AM MW', '9:35AM MW', '11:10AM MW', '1:20PM MW', '2:55PM MW', '4:30PM MW',
    '8:00AM TR', '9:35AM TR', '11:10AM TR', '1:20PM TR', '2:55PM TR', '4:30PM TR' # 6
]

def get_times(inds):
    return [class_times[idx] for idx in inds]

classes = [
    Class('CS81', get_times([6, 7]), 30, 0.5),
    Class('CS105', get_times([2, 3]), 30, 0.5),
    Class('CS124', get_times([3, 4]), 20, 0.6),
    Class('CS131', get_times([1, 2]), 30, 0.5),
    Class('CS140', get_times([3, 4]), 30, 0.5),
    Class('CS151', get_times([1]), 20, 0.5),
    Class('CS153', get_times([9, 10]), 20, 0.5),
    Class('CS159', get_times([1]), 20, 0.5),
    Class('CS181AA', get_times([9]), 20, 0.5),
    Class('CS181AB', get_times([9, 10]), 20, 0.5),
]

req_majors = {
    'CS': [classes[x] for x in [0, 1, 3, 4]],
    'CSM': [classes[x] for x in [0, 1, 4]],
}

majors = ['CS', 'CSM']      
years = ['SR', 'JR']
reg_times = ['8:00AM', '9:00AM', '10:00AM', '11:00AM', '12:00PM', '1:00PM', '2:00PM', '3:00PM']
happiness = {
    'NO': 0,
    'OPEN': 1,
    'INT': 2,
    'YAY': 3,
}

num_students = 300
exporter = Export(
    classes,
    years,
    reg_times,
    happiness,
    num_students,
    class_times
)

export_path = '../ampl_files/case-study-2.dat'

exporter.write_dat_file(export_path, np.random.choice(['CS', 'CSM'], num_students, p=[0.5, 0.5]), req_majors)

