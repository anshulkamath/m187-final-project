import csv
import numpy as np

from ClassManager import Class
from input import *

class Schedule:
    classes = []
    req_majors = {}
    happiness = []
    prob_dist = []

    def __init__(self, classes: list[Class], req_majors, happiness):
        '''
        classes is a list of classes that are offered
        req_majors is a dictionary - the key is major and the values are
            the class codes that are required for that major
        happiness is a list of possible values for student happiness
        prob_dist is a probability distribution that is parallel with the entry of classes
        '''
        self.classes = classes
        self.req_majors = req_majors
        self.happiness = happiness

    def generate_preference(self, major):
        MAJOR_BOOST = 0.1
        required: list[Class] = self.req_majors[major]
        header = [section for c in self.classes for section in c.get_sections()]

        data = { 'major': major }
        prefs = [0 for c in self.classes for _ in c.get_sections()]

        # initialize everything with a random happiness based off of prob dist
        i = 0
        for c in self.classes:
            for _ in c.get_sections():
                prob = c.get_demand()
                prefs[i] = np.random.choice(self.happiness) * np.random.choice([0, 1], p=[1 - prob, prob])
                i += 1

        # regenerate required classes for majors with small additional probability
        i = 0
        for c in required:
            for _ in c.get_sections():
                prob = c.get_demand() + MAJOR_BOOST
                prefs[i] = np.random.choice(self.happiness[1:]) * np.random.choice([0, 1], p=[1 - prob, prob])
                i += 1

        data['preferences'] = prefs
        
        return data, header

def export_data(path, data: dict):
    ''' exports data to a csv file '''
    
    with open(path, 'w+') as out:
        writer = csv.writer(out)
        
        keys = data[0].keys()
        writer.writerow(keys)
        
        for item in data:
            writer.writerow([item[key] for key in item])

def generate_csv(num_lists, path, classes, req_classes, happiness):
    '''
    generates a csv with the given information that contains a list
    of preferences for the given number of students
    '''
    schedule = Schedule(classes, req_classes, list(range(happiness)), prob_dist)
    schedules = [schedule.generate_preference(np.random.choice(['CS', 'CSM'])) for _ in range(num_lists)]

    export_data(path, schedules)
