# sets
set MAJORS;
set CLASSES;
set YEARS;
set REG_TIMES;
set HAPPINESS;
param numStudents;
set STUDENTS := 0..(numStudents-1);
set CLASS_TIMES;
set SECTIONS{CLASSES};

# params
param seats{c in CLASSES, SECTIONS[c]};                                     # how many seats per section
param req_prefs{STUDENTS, c in CLASSES, SECTIONS[c], HAPPINESS} binary;     # 1 iff a student lists the required class as a preference
param elec_prefs{STUDENTS, c in CLASSES, SECTIONS[c], HAPPINESS} binary;    # 1 iff a student lists the elective class as a preference
param class_times{c in CLASSES, SECTIONS[c], CLASS_TIMES} binary;           # 1 iff a class section is offered at the given time
param interest_rates{HAPPINESS};                                            # the weight of each happiness
param lambda;                                                               # relative weight of method

# decision variables
var x {STUDENTS, c in CLASSES, SECTIONS[c]} binary;
var minHappiness;

# objective function
maximize Happiness: lambda * (
        sum { s in STUDENTS, c in CLASSES, n in SECTIONS[c], h in HAPPINESS }
        ((elec_prefs[s, c, n, h] * interest_rates[h] + s / numStudents) * x[s, c, n])
    ) + (1 - lambda) * minHappiness;

# minimum happiness for any student
subject to Min_Happiness{s in STUDENTS}:
    minHappiness <= (sum{h in HAPPINESS, c in CLASSES, n in SECTIONS[c]} ((elec_prefs[s, c, n, h]) * interest_rates[h] * x[s, c, n]));

# cannot get same class/section in both lists
subject to Unique_List_Choice{s in STUDENTS, c in CLASSES}:
    sum {n in SECTIONS[c]} x[s, c, n] <= 1;

# cannot get 2 classes at the same time
subject to No_Overlap_Constraint{s in STUDENTS, t in CLASS_TIMES}:
    (sum {c in CLASSES, n in SECTIONS[c]} (class_times[c, n, t] * x[s, c, n])) <= 1;

# student gets into up to 2 classes
subject to Selection_Constraint_1{s in STUDENTS}: (
    sum {c in CLASSES, n in SECTIONS[c], h in HAPPINESS}
    (elec_prefs[s, c, n, h] * x[s, c, n])
) <= 2;

# student gets into only one elective
subject to Selection_Constraint_2{s in STUDENTS}: (
    sum {c in CLASSES, n in SECTIONS[c], h in HAPPINESS}
    (1 - req_prefs[s, c, n, h]) * elec_prefs[s, c, n, h] * x[s, c, n]
) <= 1;

# students constrained by the number of seats in a section
subject to Class_Size_Constraint{c in CLASSES, n in SECTIONS[c]}:
    sum{s in STUDENTS} x[s, c, n] <= seats[c, n];