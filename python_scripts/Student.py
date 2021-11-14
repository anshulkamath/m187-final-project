import csv
import numpy as np

import input as inp

class Schedule:
    classes = []
    req_majors = {}
    happiness = []
    prob_dist = []

    def __init__(self, classes, req_majors, happiness, prob_dist):
        self.classes = classes
        self.req_majors = req_majors
        self.happiness = happiness
        self.prob_dist = prob_dist

    def generate_preference(self, major):
        MAJOR_BOOST = 0.1
        required = self.req_majors[major]

        data = { 'major': major }
        prefs = len(self.classes) * [0]

        # initialize everything with a random happiness based off of prob dist
        for i in range(len(prefs)):
            prob = self.prob_dist[i]
            prefs[i] = np.random.choice(self.happiness) * np.random.choice([0, 1], p=[1 - prob, prob])

        # regenerate required classes for majors with small additional probability
        for i in required:
            prob = self.prob_dist[i] + MAJOR_BOOST
            prefs[i] = np.random.choice(self.happiness) * np.random.choice([0, 1], p=[1 - prob, prob])

        data['preferences'] = prefs

        return data

def export_data(path, data: dict):
    ''' exports data to a csv file '''
    
    with open(path, 'w+') as out:
        writer = csv.writer(out)
        
        keys = data[0].keys()
        writer.writerow(keys)
        
        for item in data:
            writer.writerow([item[key] for key in item])

def generate_csv(num_lists, path, classes, req_classes, happiness, prob_dist):
    '''
    generates a csv with the given information that contains a list
    of preferences for the given number of students
    '''
    schedule = Schedule(classes, req_classes, list(range(happiness)), prob_dist)
    schedules = [schedule.generate_preference(np.random.choice(['CS', 'CSM'])) for _ in range(num_lists)]

    export_data(path, schedules)

generate_csv(inp.num_lists, inp.path, inp.classes, inp.req_majors, inp.happiness, inp.prob_dist)
