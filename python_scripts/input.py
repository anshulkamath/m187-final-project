''' file that contains the input information for the schedule generator '''
num_lists = 100
path = './output.csv'

classes = ['CS105-01', 'CS131-01, CS131-02', 'CS140-01', 'CS140-02', 'CS124-01', 'CS124-02', 'CS153-01', 'CS153-02']
req_majors = {
    'CS': [0, 1, 2, 3, 4],
    'CSM': [1, 2, 3, 4],
}
happiness = 4
prob_dist = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5] # tweak these as per PERM data