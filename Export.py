from io import TextIOWrapper
from Student import Schedule
from ClassManager import Class

class Export():
    def __init__(self, classes: list[Class], years: list, reg_times: list, happiness: dict, num_students: int, class_times: list):
        '''
        majors: a list of majors
        classes: a dictionary where the key is a class and the value is a list of the class sections
        years: a list of class years (['JR', 'SR'])
        reg_times: a list of registration times (will be enumerated)
        '''
        self.classes = classes
        self.years = years
        self.reg_times = reg_times
        self.happiness = happiness
        self.num_students = num_students
        self.class_times = class_times

    def write_dat_file(self, path, majors, req_majors):
        enumerate_list = lambda x : [str(i) for i in range(len(x))]
        with open(path, 'w+', newline='') as out:
            # write sets
            out.write(f"set CLASSES := {' '.join([c.get_name() for c in self.classes])};\n")
            out.write(f"set YEARS := {' '.join(self.years)};\n")
            out.write(f"set REG_TIMES := {' '.join(enumerate_list(self.reg_times))};\n")
            out.write(f"set HAPPINESS := {' '.join(self.happiness)};\n")
            out.write(f"set CLASS_TIMES := {' '.join(enumerate_list(self.class_times))};\n\n")
            
            # writing sections sets
            for c in self.classes:
                out.write(f"set SECTIONS[{c.get_name()}] := {' '.join(c.get_sections())};\n")

            out.write("\n")

            # write params
            out.write(f"param numStudents := {self.num_students};\n")
            out.write(f"param interest_rates := {' '.join([' '.join([key, str(self.happiness[key])]) for key in self.happiness])};\n\n")

            # write class seat lists
            out.write("param seats :=")
            for c in self.classes:
                out.write(f"\n\t[{c.get_name()}, *] :=")
                for section in c.get_sections():
                    out.write(f" {section} {c.get_num_seats()}")
            out.write(";\n\n")

            # write class time lists
            out.write("param class_times :=")
            for c in self.classes:
                out.write(f"\n\t[{c.get_name()}, *, *] : ")
                out.write('\t'.join(enumerate_list(self.class_times)))
                out.write('\t:=')
                for section, t in c.get_times():
                    mask = [str(int(t == enum_time)) for enum_time in self.class_times]
                    str_mask = '\t'.join(mask)
                    out.write(f"\n\t{section}\t\t{str_mask}")
            
            out.write(";\n\n")

            return self.write_student_data(out, majors, req_majors)

    def write_student_data(self, writer: TextIOWrapper, majors, req_majors):
        '''
        write the req_prefs and elec_prefs using the given majors and requirements
        '''
        sched_generator = Schedule(
            self.classes,
            req_majors,
            [self.happiness[key] for key in self.happiness]
        )

        prefs = [sched_generator.generate_preference(maj)[0] for maj in majors]

        writer.write("param req_prefs :=\n")
        for i, pref in enumerate(prefs):
            required = req_majors[pref['major']]
            happiness = pref['preferences']
            
            writer.write(f"\t[{i}, *, *, *] :=")
            counter = 0
            for c in self.classes:
                for section in c.get_sections():
                    writer.write(f"\n\t\t")
                    for k, key in enumerate(self.happiness):
                        writer.write(f"{c.get_name()} {section} {key} {int(k == happiness[counter] and c in required)} ")
                    counter += 1
            writer.write(",\n")

        writer.write(";\n\n")

        writer.write("param elec_prefs :=\n")
        for i, pref in enumerate(prefs):
            happiness = pref['preferences']
            
            writer.write(f"\t[{i}, *, *, *] :=")
            counter = 0
            for c in self.classes:
                for section in c.get_sections():
                    writer.write(f"\n\t\t")
                    for k, key in enumerate(self.happiness):
                        writer.write(f"{c.get_name()} {section} {key} {int(k == happiness[counter])} ")
                    counter += 1
            writer.write(",\n")
        writer.write(";\n")
        
        return prefs
