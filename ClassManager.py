class Class():
    def __init__(self, name, section_times, num_seats, demand = 0.5):
        '''
        name - course code of the class
        section_times - the times of the section
        num_seats - the number of seats in each section of the class
        demand - the probability that a student wants to take the class
        '''
        self.name = name
        self.num_sections = len(section_times)
        self.section_times = section_times
        self.num_seats = num_seats
        self.demand = demand
    
    def get_name(self):
        ''' returns the name of the class '''
        return self.name

    def get_sections(self):
        ''' returns a list of all sections '''
        return [f'{self.name}-0{i+1}' for i in range(self.num_sections)]
    
    def get_times(self):
        ''' returns a list of all sections and their times '''
        return [[f'{self.name}-0{i+1}', self.section_times[i]] for i in range(self.num_sections)]
    
    def get_num_seats(self):
        ''' returns the number of seats in the class '''
        return self.num_seats

    def get_demand(self):
        ''' returns the demand of the class '''
        return self.demand