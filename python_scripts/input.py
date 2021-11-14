''' file that contains the input information for the schedule generator '''
from ClassManager import Class

num_lists = 100
path = './output.csv'

classes = ['CS105-01', 'CS131-01, CS131-02', 'CS140-01', 'CS140-02', 'CS124-01', 'CS124-02', 'CS153-01', 'CS153-02']
req_majors = {
    'CS': [0, 1, 2, 3, 4],
    'CSM': [1, 2, 3, 4],
}
happiness = 4
prob_dist = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5] # tweak these as per PERM data

# AMPL data

example_class_times = ['9:35AM', '10:00AM']
classes = [
    Class('CS105', example_class_times, 2), 
    Class('CS144', [example_class_times[1]], 3)
]

majors = ['CS', 'CSM']      
example_years = ['SR', 'JR']
example_reg_times = ['8:00AM', '9:00AM', '10:00AM', '11:00AM', '12:00PM', '1:00PM', '2:00PM', '3:00PM']
example_happiness = {
    'NO': 0,
    'OPEN': 1,
    'INT': 2,
    'YAY': 3,
}